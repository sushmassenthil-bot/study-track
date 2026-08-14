def insertion_sort_by_field(students, field):
    for i in range(1, len(students)):
        key = students[i]
        j = i - 1

        while j >= 0 and students[j][field] > key[field]:
            students[j + 1] = students[j]
            j -= 1

        students[j + 1] = key

    return students


def binary_search_by_name(sorted_by_name_list, name):
    low = 0
    high = len(sorted_by_name_list) - 1

    while low <= high:
        mid = low + (high - low) // 2

        current_name = sorted_by_name_list[mid]["name"]

        if current_name == name:
            return sorted_by_name_list[mid]

        if current_name < name:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def format_roster_report(students):
    lines = []

    for student in students:
        line = (
            f"[Age {student['age']}] "
            f"{student['name']} "
            f"<{student['email']}>"
        )
        lines.append(line)

    return "\n".join(lines)


def count_students_meeting_min_age(students, min_age):
    count = 0

    for student in students:
        if student["age"] >= min_age:
            count += 1

    return count