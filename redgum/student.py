"""
student.py - Student Management Module
Owner: Member A (组员A - 后端 + 项目文档)
User stories: US01 (学生注册账号) + 学生基础信息管理 (US02登录关联的学生记录)
"""
from .storage import STUDENT_FILE, load_data, save_data, next_id


class StudentManager:
    def __init__(self):
        # US07 持久化：从 data/students.json 加载学生数据
        self.students = load_data(STUDENT_FILE)

    # US01 作为学生，我可以注册账号
    def add_student(self, name, year_level, family_contact):
        """新增学生记录；必填项缺失时拒绝保存并报错"""
        if not all([name, year_level, family_contact]):
            return False, "Error: Missing required field (name/year_level/family_contact)"
        student = {
            "student_id": next_id(self.students, "student_id"),
            "name": name,
            "year_level": year_level,
            "family_contact": family_contact,
            "is_active": True,
        }
        self.students.append(student)
        save_data(STUDENT_FILE, self.students)
        return True, f"Student created. Student ID: {student['student_id']}"

    # US01 校验：重复联系方式报错（本作业以 family_contact 作唯一标识示例）
    def student_exists(self, family_contact):
        return any(s["family_contact"] == family_contact for s in self.students)

    # 学生信息修改
    def update_student(self, student_id, name=None, year_level=None, family_contact=None):
        for s in self.students:
            if s["student_id"] == student_id:
                if name:
                    s["name"] = name
                if year_level:
                    s["year_level"] = year_level
                if family_contact:
                    s["family_contact"] = family_contact
                save_data(STUDENT_FILE, self.students)
                return True, "Student updated"
        return False, "Student not found"

    # 学生停用（保留历史课程记录）
    def deactivate_student(self, student_id):
        for s in self.students:
            if s["student_id"] == student_id:
                s["is_active"] = False
                save_data(STUDENT_FILE, self.students)
                return True, "Student deactivated (history kept)"
        return False, "Student not found"

    def list_students(self):
        return self.students

    def get_student(self, student_id):
        for s in self.students:
            if s["student_id"] == student_id:
                return s
        return None
