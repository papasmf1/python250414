# 클래스 정의 및 테스트 코드 통합

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def printInfo(self):
        #f-string문법(python 3.6)
        print(f"ID: {self.id}, Name: {self.name}")

class Manager(Person):
    def __init__(self, id, name, title):
        #부모를 지칭하는 함수 
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")


# 테스트 코드

# 1. 기본 Person 인스턴스 생성 및 정보 출력
p1 = Person(1, "Alice")
p1.printInfo()
print("---")

# 2. Manager 인스턴스 생성 및 정보 출력
m1 = Manager(2, "Bob", "Team Lead")
m1.printInfo()
print("---")

# 3. Employee 인스턴스 생성 및 정보 출력
e1 = Employee(3, "Charlie", "Python")
e1.printInfo()
print("---")

# 4. Manager 객체의 멤버변수 확인
print(m1.id == 2)  # True
print(m1.name == "Bob")  # True
print(m1.title == "Team Lead")  # True
print("---")

# 5. Employee 객체의 멤버변수 확인
print(e1.id == 3)  # True
print(e1.name == "Charlie")  # True
print(e1.skill == "Python")  # True
print("---")

# 6. Manager는 Person의 인스턴스인가?
print(isinstance(m1, Person))  # True

# 7. Employee는 Person의 인스턴스인가?
print(isinstance(e1, Person))  # True
print("---")

# 8. Manager의 printInfo() 오버라이딩 확인
m2 = Manager(4, "Dana", "CTO")
m2.printInfo()
print("---")

# 9. Employee의 printInfo() 오버라이딩 확인
e2 = Employee(5, "Eve", "Data Analysis")
e2.printInfo()
print("---")

# 10. 다양한 객체를 리스트에 담아 반복 출력
people = [p1, m1, e1, m2, e2]
for person in people:
    person.printInfo()
    print("---")
