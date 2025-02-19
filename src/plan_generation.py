from ortools.sat.python import cp_model


def generate_plan(
    schueler_wahlen,
    firmen_kapazitaet,
    klassen_grenze,
    slots_pro_block,
    schueler_klassen,
) -> list[dict]:
    model = cp_model.CpModel()

    zuweisung = {}
    for schueler, wahlen in schueler_wahlen.items():
        for block in ["block1", "block2"]:
            for slot in range(slots_pro_block):
                for firma in wahlen[block]:
                    # Erstelle eine Binärvariable für die Zuordnung (1 = Schüler ist in dem Slot bei der Firma)
                    zuweisung[(schueler, block, slot, firma)] = model.NewBoolVar(
                        f"{schueler}_{block}_slot{slot}_firma{firma}"
                    )

    # Einschränkungen definieren
    for schueler, wahlen in schueler_wahlen.items():
        # Jeder Schüler muss genau 1 Firma pro Slot in jedem Block besuchen
        for block in ["block1", "block2"]:
            for slot in range(slots_pro_block):
                # Der Schüler muss genau 1 Firma in diesem Slot in diesem Block besuchen
                model.Add(
                    sum(
                        zuweisung[(schueler, block, slot, firma)]
                        for firma in schueler_wahlen[schueler][block]
                    )
                    == 1
                )

    # Einschränkung der Kapazität: Keine Firma darf mehr als ihre Kapazität Schüler in einem Slot haben
    for block in ["block1", "block2"]:
        for slot in range(slots_pro_block):
            for firma, kapazitaet in firmen_kapazitaet.items():
                # Die Summe der Schüler, die Firma in diesem Slot besuchen, darf die Kapazität nicht überschreiten
                model.Add(
                    sum(
                        zuweisung[(schueler, block, slot, firma)]
                        for schueler in schueler_wahlen
                        if firma in schueler_wahlen[schueler][block]
                    )
                    <= kapazitaet
                )

    # Einschränkung der Klassengröße: Maximal 4 Schüler aus derselben Klasse in einem Vortrag
    for block in ["block1", "block2"]:
        for slot in range(slots_pro_block):
            for firma in firmen_kapazitaet.keys():
                # Für jede Klasse: Maximal 4 Schüler pro Vortrag in diesem Slot
                for klasse in set(schueler_klassen.values()):
                    model.Add(
                        sum(
                            zuweisung[(schueler, block, slot, firma)]
                            for schueler in schueler_wahlen
                            if firma in schueler_wahlen[schueler][block]
                            and schueler_klassen[schueler] == klasse
                        )
                        <= klassen_grenze
                    )

    # Einschränkung: Jeder Schüler darf eine Firma nur einmal pro Block besuchen
    for schueler, wahlen in schueler_wahlen.items():
        for block in ["block1", "block2"]:
            for firma in wahlen[block]:
                # Ein Schüler darf eine Firma nur einmal pro Block besuchen
                model.Add(
                    sum(
                        zuweisung[(schueler, block, slot, firma)]
                        for slot in range(slots_pro_block)
                    )
                    <= 1
                )

    # Lösen des Modells
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Ergebnis ausgeben
    content = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for schueler, wahlen in schueler_wahlen.items():
            point = {}
            point["name"] = schueler
            point["klasse"] = schueler_klassen[schueler]
            for block in ["block1", "block2"]:
                for slot in range(slots_pro_block):
                    for firma in wahlen[block]:
                        if solver.Value(zuweisung[(schueler, block, slot, firma)]):
                            key = f"{block}_{slot+1}"
                            point[key] = firma
            content.append(point)
    return content
