# Redgum Tutoring System

辅导中心排课与课时追踪系统（Scrum 小组作业：Sprint1 + Sprint2）
Python 命令行应用，JSON 文件持久化。

## 运行要求
- Python 3.8+

## 运行方式
```bash
cd redgum-tutoring
python -m redgum.main
```
运行后自动在 `data/` 目录生成 `students.json`、`tutors.json`、`availability.json`、`sessions.json`，重启程序数据不丢失。

## 代码模块与组员分工（GitHub 协作用）

| 模块文件 | 组员 | 用户故事 | 职责 |
|---------|------|---------|------|
| `redgum/storage.py` | 组员A | US07 通用 | 数据读写、持久化工具 |
| `redgum/student.py` | 组员A | US01, US02 | 学生注册、信息管理 |
| `redgum/tutor.py` | 组员B | US03, US04 | 导师列表、可用时段 |
| `redgum/booking.py` | 组员C | US04, US05, US06, US08 | 预约、修改/取消、时间校验、视图 |
| `redgum/main.py` | 全体集成 | — | 演示入口 |

## GitHub 协作流程（分支模型）
1. 组员A 创建仓库，初始化 `main` 分支，提交 `storage.py` 与 `__init__.py`。
2. 每个组员从 `main` 拉取最新代码，创建自己的分支：
   - 组员A：`feature/student`
   - 组员B：`feature/tutor`
   - 组员C：`feature/booking`
3. 各自开发自己的模块文件，Push 到自己的分支。
4. 组员A 作为集成负责人，把三个分支 **Merge 到 main**；有冲突时三人一起解决。
5. 所有人各自在 main 上拉取合并结果，运行 `python -m redgum.main` 验证集成。

## 命令速查
```bash
git checkout -b feature/student
git add redgum/student.py
git commit -m "US01: add student registration"
git push origin feature/student
```
