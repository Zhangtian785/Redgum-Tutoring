"""
main.py - System Integration & Demo Entry
Integrated by: all members (每人负责集成自己模块的调用)
运行方式：在 redgum-tutoring 目录下执行  python -m redgum.main
"""
from .storage import STUDENT_FILE, TUTOR_FILE, AVAIL_FILE, SESSION_FILE
from .student import StudentManager
from .tutor import TutorManager
from .booking import SessionManager


def demo():
    print("=" * 50)
    print("Redgum Tutoring System - Full Demo")
    print("=" * 50)

    student_mgr = StudentManager()   # Member A module
    tutor_mgr = TutorManager()       # Member B module
    session_mgr = SessionManager(tutor_mgr, student_mgr)  # Member C module

    # ---- Member A: Student (US01) ----
    print("\n[1] US01 Add Student")
    print(student_mgr.add_student("Liam", "Year 10", "0401-123456"))
    print(student_mgr.add_student("Mia", "Year 11", "0402-654321"))

    # ---- Member B: Tutor + Availability (US03, US04) ----
    print("\n[2] US03 Add Tutor & US04 Availability")
    print(tutor_mgr.add_tutor("Tomas", ["Physics", "Chemistry", "Maths"]))
    print(tutor_mgr.add_tutor("Sofia", ["English", "Biology"]))
    print(tutor_mgr.add_availability(1, "Wednesday", "15:30", "18:00"))
    print(tutor_mgr.add_availability(2, "Wednesday", "16:00", "19:00"))

    # ---- Member C: Booking + Validation (US04/US08) ----
    print("\n[3] US04 Create Session (valid time)")
    print(session_mgr.create_session(1, 1, "2026-10-07", "16:00", 60))  # Wednesday

    print("\n[4] US08 Reject: outside availability")
    print(session_mgr.create_session(1, 1, "2026-10-07", "09:00", 60))  # outside window

    print("\n[5] US08 Reject: tutor time conflict")
    print(session_mgr.create_session(2, 1, "2026-10-07", "16:30", 60))  # same tutor busy

    # ---- Member C: US05 modify / cancel ----
    print("\n[6] US05 Cancel session (record kept)")
    print(session_mgr.cancel_session(1))
    print("Sessions after cancel:", session_mgr.sessions)

    print("\nDemo finished. Data persisted in data/*.json")


if __name__ == "__main__":
    demo()
