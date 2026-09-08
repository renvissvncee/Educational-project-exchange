from datetime import date

student_name = "Иван"
project_name = "Учебный проект"
participants_text = "2"
participants = int(participants_text)
project_ready = True
publication_date = date.today()

print("Студент:", student_name)
print("Проект:", project_name)
print("Количество участников:", participants)
print("Дата:", publication_date)

if project_ready and participants > 0:
	print("Проект можно разместить на бирже")
else:
	print("Проект пока нельзя разместить")
