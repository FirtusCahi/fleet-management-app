from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def export_to_pdf(filepath, vehicles, drivers, expenses, missions, assignments, lang, for_print=False):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(lang.get("report_title", "Rapport de Gestion de Flotte"), styles['h1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # --- Vehicles ---
    story.append(Paragraph(lang.get("report_vehicles", "Véhicules"), styles['h2']))
    if vehicles:
        data = [[lang.get("registration", "Immatriculation"), lang.get("make", "Marque"), lang.get("model", "Modèle"), lang.get("year", "Année"), lang.get("revision_date_short", "Révision"), lang.get("control_date_short", "Contrôle")]]
        for vehicle in vehicles:
            data.append([str(v) for v in vehicle[1:]])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)
    else:
        story.append(Paragraph(lang.get("report_no_vehicles", "Aucun véhicule enregistré."), styles['normal']))
    story.append(Spacer(1, 12))

    # --- Drivers ---
    story.append(Paragraph(lang.get("report_drivers", "Conducteurs"), styles['h2']))
    if drivers:
        data = [[lang.get("name", "Nom"), lang.get("surname", "Prénom"), lang.get("license_number", "Numéro de permis"), lang.get("expiry_date_short", "Expiration")]]
        for driver in drivers:
            data.append([str(d) for d in driver[1:]])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)
    else:
        story.append(Paragraph(lang.get("report_no_drivers", "Aucun conducteur enregistré."), styles['normal']))
    story.append(Spacer(1, 12))

    # --- Expenses ---
    story.append(Paragraph(lang.get("report_expenses", "Dépenses"), styles['h2']))
    if expenses:
        data = [[lang.get("vehicle", "Véhicule"), lang.get("date", "Date"), lang.get("type", "Type"), lang.get("amount", "Montant"), lang.get("description", "Description")]]
        for expense in expenses:
            vehicle = database.get_vehicle(None, expense[1]) # Need a connection if not in the same scope
            vehicle_reg = vehicle[1] if vehicle else lang.get("unknown", "Inconnu")
            data.append([vehicle_reg, expense[2], expense[3], f"{expense[4]:.2f}", expense[5]])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)
    else:
        story.append(Paragraph(lang.get("report_no_expenses", "Aucune dépense enregistrée."), styles['normal']))
    story.append(Spacer(1, 12))

    # --- Missions ---
    story.append(Paragraph(lang.get("report_missions", "Missions"), styles['h2']))
    if missions:
        data = [[lang.get("driver", "Conducteur"), lang.get("start_date_short", "Début"), lang.get("end_date_short", "Fin"), lang.get("destination", "Destination"), lang.get("duration_short", "Durée"), lang.get("meals_short", "Repas"), lang.get("nights_short", "Nuits"), lang.get("weekends_short", "WE")]]
        for mission in missions:
            driver = database.get_driver(None, mission[1]) # Need a connection if not in the same scope
            driver_name = f"{driver[1]} {driver[2]}" if driver else lang.get("unknown", "Inconnu")
            data.append([driver_name, mission[2], mission[3], mission[4], str(mission[5]), str(mission[6]), str(mission[7]), str(mission[8])])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)
    else:
        story.append(Paragraph(lang.get("report_no_missions", "Aucune mission enregistrée."), styles['normal']))
    story.append(Spacer(1, 12))

    # --- Assignments ---
    story.append(Paragraph(lang.get("report_assignments", "Affectations"), styles['h2']))
    if assignments:
        data = [[lang.get("vehicle", "Véhicule"), lang.get("driver", "Conducteur"), lang.get("assignment_date_short", "Date")]]
        for assignment in assignments:
            data.append([assignment[1], f"{assignment[2]} {assignment[3]}", assignment[4]])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)
    else:
        story.append(Paragraph(lang.get("report_no_assignments", "Aucune affectation enregistrée."), styles['normal']))
    story.append(Spacer(1, 12))

    doc.build(story)