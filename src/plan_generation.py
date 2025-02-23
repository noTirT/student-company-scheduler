import random


def generate_plan_custom(
    schueler_wahlen,
    firmen_kapazitaet,
    klassen_grenze,
    slots_pro_block,
    schueler_klassen,
) -> list[dict]:
    total_slots = slots_pro_block * 2

    result = {
        student: ["" for _ in range(slots_pro_block * 2)] for student in schueler_wahlen
    }

    # Track remaining capacities for each company
    remaining_capacity = [
        {company: firmen_kapazitaet[company] for company in firmen_kapazitaet}
        for _ in range(total_slots)
    ]

    # Track how many students of each class are assigned to a company per slot
    class_count_per_slot = [
        {company: {} for company in firmen_kapazitaet}
        for _ in range(slots_pro_block * 2)
    ]

    # Track which companies a student has already attended
    student_attendance = {student: set() for student in schueler_wahlen}

    students = list(schueler_wahlen.keys())
    random.shuffle(students)  # Shuffle students for fairness

    for block_index, block_name in enumerate(["block1", "block2"]):
        for slot in range(slots_pro_block):
            slot_index = block_index * slots_pro_block + slot

            for student in students:
                wishes = schueler_wahlen[student][block_name]
                student_class = schueler_klassen[student]

                random.shuffle(wishes)  # Shuffle preferences for fairness

                for company in wishes:
                    if (
                        remaining_capacity[slot_index][company] > 0
                        and company not in student_attendance[student]
                    ):
                        class_count = class_count_per_slot[slot_index][company]

                        if class_count.get(student_class, 0) < klassen_grenze:
                            # Assign student
                            result[student][slot_index] = company
                            remaining_capacity[slot_index][company] -= 1
                            class_count[student_class] = (
                                class_count.get(student_class, 0) + 1
                            )
                            student_attendance[student].add(company)
                            break  # Move to next student

    parsed_result = []
    for name, choices in result.items():
        parsed_object = {}
        parsed_object["name"] = name
        parsed_object["klasse"] = schueler_klassen[name]
        parsed_object["1_1"] = choices[0]

        parsed_object["1_2"] = choices[1]
        parsed_object["2_1"] = choices[2]
        parsed_object["2_2"] = choices[3]

        parsed_result.append(parsed_object)

    return parsed_result
