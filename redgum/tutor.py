"""
tutor.py - Tutor & Availability Management Module
Owner: Member B (组员B - 前端 + ER图/数据模型)
User stories: US03 (浏览导师列表), US04 (导师可用时间段 Availability)
"""
from .storage import TUTOR_FILE, AVAIL_FILE, load_data, save_data, next_id


class TutorManager:
    def __init__(self):
        # US07 持久化：加载导师数据 + 可用时段数据
        self.tutors = load_data(TUTOR_FILE)
        self.availability = load_data(AVAIL_FILE)

    # US03 作为学生，我可以浏览导师列表
    def add_tutor(self, name, subjects):
        """新增导师，记录授课科目"""
        if not name:
            return False, "Error: Tutor name required"
        tutor = {
            "tutor_id": next_id(self.tutors, "tutor_id"),
            "name": name,
            "subjects": subjects,
            "is_active": True,
        }
        self.tutors.append(tutor)
        save_data(TUTOR_FILE, self.tutors)
        return True, f"Tutor created. Tutor ID: {tutor['tutor_id']}"

    # 导师信息修改（维护授课科目）
    def update_tutor(self, tutor_id, name=None, subjects=None):
        for t in self.tutors:
            if t["tutor_id"] == tutor_id:
                if name:
                    t["name"] = name
                if subjects:
                    t["subjects"] = subjects
                save_data(TUTOR_FILE, self.tutors)
                return True, "Tutor updated"
        return False, "Tutor not found"

    # 停用离职导师：不删除历史课程记录；停用后不出现在新建预约可选列表
    def deactivate_tutor(self, tutor_id):
        for t in self.tutors:
            if t["tutor_id"] == tutor_id:
                t["is_active"] = False
                save_data(TUTOR_FILE, self.tutors)
                return True, "Tutor deactivated (history kept)"
        return False, "Tutor not found"

    def get_active_tutors(self):
        """只返回在职导师（停用导师不进入新建预约列表）"""
        return [t for t in self.tutors if t["is_active"]]

    # US04 维护导师可用时间段 Availability
    def add_availability(self, tutor_id, weekday, start_time, end_time):
        """给导师添加一个可用时间段"""
        tutor = self.get_tutor(tutor_id)
        if tutor is None:
            return False, "Tutor not found"
        avail = {
            "availability_id": next_id(self.availability, "availability_id"),
            "tutor_id": tutor_id,
            "weekday": weekday,
            "start_time": start_time,
            "end_time": end_time,
        }
        self.availability.append(avail)
        save_data(AVAIL_FILE, self.availability)
        return True, "Availability window added"

    # 编辑/删除已有可用时段
    def update_availability(self, availability_id, weekday=None, start_time=None, end_time=None):
        for a in self.availability:
            if a["availability_id"] == availability_id:
                if weekday:
                    a["weekday"] = weekday
                if start_time:
                    a["start_time"] = start_time
                if end_time:
                    a["end_time"] = end_time
                save_data(AVAIL_FILE, self.availability)
                return True, "Availability updated"
        return False, "Availability not found"

    def remove_availability(self, availability_id):
        before = len(self.availability)
        self.availability = [a for a in self.availability if a["availability_id"] != availability_id]
        save_data(AVAIL_FILE, self.availability)
        return (True, "Availability removed") if len(self.availability) < before else (False, "Availability not found")

    def get_tutor(self, tutor_id):
        for t in self.tutors:
            if t["tutor_id"] == tutor_id:
                return t
        return None

    def get_tutor_availability(self, tutor_id):
        """返回某导师的全部可用时段（US04 核心数据，供预约校验使用）"""
        return [a for a in self.availability if a["tutor_id"] == tutor_id]
