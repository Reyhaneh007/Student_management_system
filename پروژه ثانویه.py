import numpy as np


class Person:
    def __init__(self, name: str, national_id: str):
        self.name = name
        self.national_id = national_id

    def display_info(self):
        return f"نام: {self.name} | کد ملی: {self.national_id}"


class Course:
    def __init__(self, course_code: str, title: str, credits: int):
        self.course_code = course_code
        self.title = title
        self.credits = credits

    def __str__(self):
        return f"{self.title} ({self.course_code}) - {self.credits} واحد"


class Student(Person):
    total_students = 0

    def __init__(self, student_id: str, name: str, national_id: str):
        super().__init__(name, national_id)
        self.student_id = student_id
        self.courses = {}
        Student.total_students += 1

    @property
    def gpa(self) -> float:
        if not self.courses:
            return 0.0
        total_points = sum(grade * course.credits for course, grade in self.courses.values())
        total_credits = sum(course.credits for course, _ in self.courses.values())
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    @property
    def total_credits(self) -> int:
        return sum(course.credits for course, _ in self.courses.values())

    def add_grade(self, course: Course, grade: float):
        self.courses[course.course_code] = (course, grade)

    def display_info(self):
        base_info = super().display_info()
        return f"شماره دانشجویی: {self.student_id} | {base_info} | معدل: {self.gpa}"

    def __str__(self):
        return f"دانشجو: {self.name} ({self.student_id}) - معدل: {self.gpa}"

    def __repr__(self):
        return f"Student('{self.student_id}', '{self.name}', '{self.national_id}')"

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False


class EducationalManager:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, student: Student):
        self.students[student.student_id] = student

    def remove_student(self, student_id: str):
        if student_id in self.students:
            del self.students[student_id]
            Student.total_students -= 1
            return True
        return False

    def add_course(self, course: Course):
        self.courses[course.course_code] = course

    def register_grade(self, student_id: str, course_code: str, grade: float):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            student.add_grade(course, grade)
            return True
        return False

    def get_transcript(self, student_id: str) -> str:
        if student_id not in self.students:
            return "دانشجو یافت نشد."
        
        student = self.students[student_id]
        lines = [f"\n=== کارنامه دانشجو: {student.name} ({student.student_id}) ==="]
        for course_code, (course, grade) in student.courses.items():
            lines.append(f"- {course.title} ({course.credits} واحد): {grade}")
        lines.append(f"کل واحدها: {student.total_credits}")
        lines.append(f"معدل کل: {student.gpa}")
        lines.append("=" * 40)
        return "\n".join(lines)

    @staticmethod
    def bubble_sort(arr, key=lambda x: x):
        n = len(arr)
        arr_copy = arr.copy()
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if key(arr_copy[j]) > key(arr_copy[j + 1]):
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    swapped = True
            if not swapped:
                break
        return arr_copy

    def sort_students(self, by="gpa", reverse=True):
        students_list = list(self.students.values())
        
        if by == "gpa":
            key_func = lambda s: s.gpa
        elif by == "credits":
            key_func = lambda s: s.total_credits
        elif by == "name":
            key_func = lambda s: s.name
        else:
            raise ValueError("معیار مرتب‌سازی نامعتبر است.")

        sorted_list = self.bubble_sort(students_list, key=key_func)
        if reverse:
            sorted_list.reverse()
        return sorted_list

    def analyze_grades(self, passing_grade=10.0):
        all_grades = []
        for student in self.students.values():
            for _, grade in student.courses.values():
                all_grades.append(grade)

        if not all_grades:
            return None

        grades_array = np.array(all_grades)

        mean_val = np.mean(grades_array)
        max_val = np.max(grades_array)
        min_val = np.min(grades_array)
        std_val = np.std(grades_array)
        passed_count = np.sum(grades_array >= passing_grade)
        failed_count = np.sum(grades_array < passing_grade)

        return {
            "میانگین نمرات": round(float(mean_val), 2),
            "بیشترین نمره": float(max_val),
            "کمترین نمره": float(min_val),
            "انحراف معیار": round(float(std_val), 2),
            "تعداد قبولی": int(passed_count),
            "تعداد مردودی": int(failed_count)
        }


def run_interactive_menu():
    system = EducationalManager()

    while True:
        print("\n=== سیستم مدیریت آموزشی ===")
        print("1. افزودن درس جدید")
        print("2. افزودن دانشجوی جدید")
        print("3. ثبت نمره برای دانشجو")
        print("4. مشاهده کارنامه دانشجو")
        print("5. مشاهده لیست دانشجویان (مرتب‌شده بر اساس معدل)")
        print("6. تحلیل آماری نمرات")
        print("7. خروج")

        choice = input("لطفا گزینه مورد نظر را انتخاب کنید (1-7): ").strip()

        if choice == "1":
            code = input("کد درس: ").strip()
            title = input("عنوان درس: ").strip()
            try:
                credits = int(input("تعداد واحد: ").strip())
                system.add_course(Course(code, title, credits))
                print(f"درس '{title}' با موفقیت ثبت شد.")
            except ValueError:
                print("خطا: تعداد واحد باید یک عدد صحیح باشد.")

        elif choice == "2":
            s_id = input("شماره دانشجویی: ").strip()
            name = input("نام و نام خانوادگی: ").strip()
            n_id = input("کد ملی: ").strip()
            system.add_student(Student(s_id, name, n_id))
            print(f"دانشجو '{name}' با موفقیت ثبت شد.")

        elif choice == "3":
            s_id = input("شماره دانشجویی: ").strip()
            c_code = input("کد درس: ").strip()
            try:
                grade = float(input("نمره: ").strip())
                if system.register_grade(s_id, c_code, grade):
                    print("نمره با موفقیت ثبت شد.")
                else:
                    print("خطا: شماره دانشجویی یا کد درس در سیستم یافت نشد.")
            except ValueError:
                print("خطا: نمره باید یک عدد اعشاری یا صحیح باشد.")

        elif choice == "4":
            s_id = input("شماره دانشجویی دانشجو: ").strip()
            print(system.get_transcript(s_id))

        elif choice == "5":
            if not system.students:
                print("هنوز هیچ دانشجویی ثبت نشده است.")
            else:
                print("\n--- لیست دانشجویان (مرتب‌شده بر اساس معدل) ---")
                sorted_students = system.sort_students(by="gpa", reverse=True)
                for student in sorted_students:
                    print(student)

        elif choice == "6":
            stats = system.analyze_grades()
            if stats is None:
                print("هیچ نمره‌ای در سیستم ثبت نشده است.")
            else:
                print("\n--- تحلیل آماری نمرات کل سیستم ---")
                for k, v in stats.items():
                    print(f"{k}: {v}")

        elif choice == "7":
            print("با تشکر، از برنامه خارج شدید.")
            break
        else:
            print("گزینه نامعتبر است. لطفا عددی بین 1 تا 7 وارد کنید.")


if __name__ == "__main__":
    run_interactive_menu()
