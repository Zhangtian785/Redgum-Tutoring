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
