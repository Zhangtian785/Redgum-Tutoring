"""
booking.py - Session Booking & Validation Module
Owner: Member C (组员C - 测试 + 评审/交付文档)
User stories:
  US04 新建预约 + 时间校验 (复用)
  US05 修改/取消预约
  US06 导师查看自己即将到来的课程
  US08 时间冲突校验
"""
from datetime import datetime, timedelta

from .storage import SESSION_FILE, load_data, save_data, next_id


class SessionManager:
    def __init__(self, tutor_manager, student_manager):
        self.sessions = load_data(SESSION_FILE)
        self.tutor_mgr = tutor_manager
        self.student_mgr = student_manager

    # ============ 时间校验工具（US08 核心逻辑）============
    def _is_time_in_availability(self, tutor_id, weekday, start_time, end_time):
        """检查某时间段是否完全落在导师可用时段内（US08 时间校验）"""
        avail_list = self.tutor_mgr.get_tutor_availability(tutor_id)
        for avail in avail_list:
            if avail["weekday"].lower() == weekday.lower():
                a_start = datetime.strptime(avail["start_time"], "%H:%M").time()
                a_end = datetime.strptime(avail["end_time"], "%H:%M").time()
                s_start = datetime.strptime(start_time, "%H:%M").time()
                s_end = datetime.strptime(end_time, "%H:%M").time()
                if s_start >= a_start and s_end <= a_end:
                    return True
        return False

    def _tutor_busy(self, tutor_id, session_date, start_time, end_time, exclude_id=None):
        """检查该导师在同一时间是否已有未取消预约（US08 防重复冲突）"""
        for sess in self.sessions:
            if sess["tutor_id"] == tutor_id and sess["session_date"] == session_date \
                    and sess["status"] != "cancelled" and sess["session_id"] != exclude_id:
                s_start = datetime.strptime(sess["start_time"], "%H:%M").time()
                s_end_dt = datetime.strptime(sess["start_time"], "%H:%M") + timedelta(minutes=sess["duration_min"])
                s_end = s_end_dt.time()
                new_start = datetime.strptime(start_time, "%H:%M").time()
                new_end = datetime.strptime(end_time, "%H:%M").time()
                if not (new_end <= s_start or new_start >= s_end):  # 时间段重叠
                    return True
        return False

    # ============ US04 新建预约 + 时间校验 ============
    def create_session(self, student_id, tutor_id, session_date, start_time, duration_min):
        """新建预约：必须落在导师可用时段内，且不与已有预约冲突"""
        if self.student_mgr.get_student(student_id) is None:
            return False, "Error: Student not found"
        if self.tutor_mgr.get_tutor(tutor_id) is None:
            return False, "Error: Tutor not found"

        date_obj = datetime.strptime(session_date, "%Y-%m-%d")
        weekday = date_obj.strftime("%A")
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = start_dt + timedelta(minutes=duration_min)
        session_end = end_dt.strftime("%H:%M")

        # US08：时间必须落在导师可用时段内
        if not self._is_time_in_availability(tutor_id, weekday, start_time, session_end):
            return False, "Rejected: Session time outside tutor available window"
        # US08：导师同一时间不能有冲突预约
        if self._tutor_busy(tutor_id, session_date, start_time, session_end):
            return False, "Rejected: Tutor already booked at this time (time conflict)"

        session = {
            "session_id": next_id(self.sessions, "session_id"),
            "student_id": student_id,
            "tutor_id": tutor_id,
            "session_date": session_date,
            "start_time": start_time,
            "duration_min": duration_min,
            "status": "booked",
        }
        self.sessions.append(session)
        save_data(SESSION_FILE, self.sessions)
        return True, f"Session booked. Session ID: {session['session_id']}"

    # ============ US05 修改/取消预约 ============
    def update_session(self, session_id, new_date=None, new_start=None, new_duration=None):
        """修改预约时间：修改后的时间仍须通过可用时段与冲突校验"""
        for sess in self.sessions:
            if sess["session_id"] == session_id:
                if new_date:
                    sess["session_date"] = new_date
                if new_start:
                    sess["start_time"] = new_start
                if new_duration:
                    sess["duration_min"] = new_duration

                date_obj = datetime.strptime(sess["session_date"], "%Y-%m-%d")
                weekday = date_obj.strftime("%A")
                start_dt = datetime.strptime(sess["start_time"], "%H:%M")
                end_dt = start_dt + timedelta(minutes=sess["duration_min"])
                session_end = end_dt.strftime("%H:%M")

                if not self._is_time_in_availability(sess["tutor_id"], weekday, sess["start_time"], session_end):
                    return False, "Update failed: new time outside tutor availability window"
                if self._tutor_busy(sess["tutor_id"], sess["session_date"], sess["start_time"], session_end, exclude_id=session_id):
                    return False, "Update failed: time conflict with another session"

                save_data(SESSION_FILE, self.sessions)
                return True, "Session updated successfully"
        return False, "Session not found"

    def cancel_session(self, session_id):
        """取消预约：记录保留（status=cancelled），不删除数据"""
        for sess in self.sessions:
            if sess["session_id"] == session_id:
                sess["status"] = "cancelled"
                save_data(SESSION_FILE, self.sessions)
                return True, "Session cancelled (record kept)"
        return False, "Session not found"

    # ============ US06 导师查看自己即将到来的课程 ============
    def get_tutor_upcoming_sessions(self, tutor_id):
        """返回某导师未来未取消的预约（只含自己的课程，不含别人的）"""
        today = datetime.now().date()
        result = []
        for sess in self.sessions:
            sess_date = datetime.strptime(sess["session_date"], "%Y-%m-%d").date()
            if sess["tutor_id"] == tutor_id and sess["status"] == "booked" and sess_date >= today:
                result.append(sess)
        return result

    # 中心课表视图（按天/周）
    def get_sessions_by_day(self, target_date):
        return [s for s in self.sessions if s["session_date"] == target_date]

    def get_sessions_by_week(self, start_week_date):
        start = datetime.strptime(start_week_date, "%Y-%m-%d").date()
        end = start + timedelta(days=6)
        return [s for s in self.sessions
                if start <= datetime.strptime(s["session_date"], "%Y-%m-%d").date() <= end]

    # 单个学生的历史和未来课程
    def get_student_all_sessions(self, student_id):
        return [s for s in self.sessions if s["student_id"] == student_id]
