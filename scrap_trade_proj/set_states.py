from state_wf.models import StepState, StepStateTranslation

#----------------  offer_new
r0 = StepState.objects.filter(state_key='offer_new')
if r0.count() < 1:
    new_0 = StepState(
        state_key = 'offer_new',
        security_level = 0,
        group_key = 1,
        group_serial_number = 1,
        manual_set = False,
        is_alert_button = False,
    )
    new_0.save()
    new_0.save()
    t_en_0 = StepStateTranslation(
        state_name = "New offer",
        state_name_plural = "New offers",
        state_description = "new offer state",
        model = new_0,
        language = 'en'
    )
    t_en_0.save()
    t_de_0 = StepStateTranslation(
        state_name = "Neues Angebot",
        state_name_plural = "Neue Angebote",
        state_description = "neues angebot",
        model = new_0,
        language = 'de',
    )
    t_de_0.save()
    t_cs_0 = StepStateTranslation(
        state_name = "Nová nabídka",
        state_name_plural = "Nové nabídky",
        state_description = "nova nabidka",
        model = new_0,
        language = 'cs'
    )
    t_cs_0.save()

#----------------  offer_confirmed
r1 = StepState.objects.filter(state_key='offer_confirmed')
if r1.count() < 1:
    new_1 = StepState(
        state_key = 'offer_confirmed',
        security_level = 0,
        group_key = 1,
        group_serial_number = 2,
        manual_set = True,
        is_alert_button = False
    )
    new_1.save()
    add_1 = StepState.objects.filter(state_key='offer_new').first()
    new_1.previous.add(add_1)
    new_1.save()
    t_en_1 = StepStateTranslation(
        state_name = "Confirmed offer",
        state_name_plural = "Confirmed offers",
        state_description = "confirmed offer",
        state_button_text = "Confirm offer",
        state_template_title = "Offer confirmation",
        state_template_question = 'Are you sure, you want confirm offer',
        state_template_text = "If you confirm offer, you can't change it and you must contact poweruser.",
        state_template_confitm_button = "Yes, Confirm",
        state_template_cancel_button = "Cancel",
        model = new_1,
        language = 'en'
    )
    t_en_1.save()
    t_de_1 = StepStateTranslation(
        state_name = "Bestätigtes Angebot",
        state_name_plural = "Bestätigte Angebote",
        state_description = "bestätigtes angebot",
        state_button_text = "Angebot bestätigen",
        state_template_title = "Angebots Bestätigung",
        state_template_question = 'Sind Sie sicher, Sie wollen das Angebot bestätigen',
        state_template_text = "Wenn Sie Angebot bestätigen, können Sie es nicht ändern und Sie müssen poweruser Kontaktieren.",
        state_template_confitm_button = "Ja, Bestätigen",
        state_template_cancel_button = "Stornieren",
        model = new_1,
        language = 'de'
    )
    t_de_1.save()
    t_cs_1 = StepStateTranslation(
        state_name = "Potvrzená nabídka",
        state_name_plural = "Potvrzené nabídky",
        state_description = "potvrzená nabídka",
        state_button_text = "Potvrdit nabídku",
        state_template_title = "Potvrzení nabídky",
        state_template_question = 'Jste si jistý, že chete potvrdit nabídku',
        state_template_text = "Když potvrdíte nabídku, nemůžete jí dále měnit a musíte kontaktovat super uživatele.",
        state_template_confitm_button = "Ano, potvrdit",
        state_template_cancel_button = "Zrušit",
        model = new_1,
        language = 'cs',
    )
    t_cs_1.save()

#----------------  offer_in_auction
r2 = StepState.objects.filter(state_key='offer_in_auction')
if r2.count() < 1:
    new_2 = StepState(
        state_key = 'offer_in_auction',
        security_level = 0,
        group_key = 1,
        group_serial_number = 3,
        manual_set = False,
        is_alert_button = False,
    )
    new_2.save()
    add_2 = StepState.objects.filter(state_key='offer_confirmed').first()
    new_2.previous.add(add_2)
    new_2.save()
    t_en_2 = StepStateTranslation(
        state_name = "Offer in auction",
        state_name_plural = "Offers in auction",
        state_description = "offer in auction",
        model = new_2,
        language = 'en'
    )
    t_en_2.save()
    t_de_2 = StepStateTranslation(
        state_name = "Angebot in der Auktion",
        state_name_plural = "Angebote in der Auktion",
        state_description = "angebot in der auktion",
        model = new_2,
        language = 'de'
    )
    t_de_2.save()
    t_cs_2 = StepStateTranslation(
        state_name = "Nabídka v aukci",
        state_name_plural = "Nabídky v aukci",
        state_description = "nabídka v aukci",
        model = new_2,
        language = 'cs'
    )
    t_cs_2.save()

#----------------  offer_accepted
r2 = StepState.objects.filter(state_key='offer_accepted')
if r2.count() < 1:
    new_2 = StepState(
        state_key = 'offer_accepted',
        security_level = 0,
        group_key = 1,
        group_serial_number = 4,
        manual_set = False,
        is_alert_button = False,
    )
    new_2.save()
    add_2 = StepState.objects.filter(state_key='offer_in_auction').first()
    new_2.previous.add(add_2)
    new_2.save()
    t_en_2 = StepStateTranslation(
        state_name = "Accepted offer",
        state_name_plural = "Accepted offers",
        state_description = "accepted offer",
        model = new_2,
        language = 'en'
    )
    t_en_2.save()
    t_de_2 = StepStateTranslation(
        state_name = "Akzeptiertes Angebot",
        state_name_plural = "Akzeptierte Angebote",
        state_description = "akzeptierte angebot",
        model = new_2,
        language = 'de'
    )
    t_de_2.save()
    t_cs_2 = StepStateTranslation(
        state_name = "Přijatá nabídka",
        state_name_plural = "Přijaté nabídky",
        state_description = "přijatá nabídka",
        model = new_2,
        language = 'cs'
    )
    t_cs_2.save()

#----------------  offer_ready_to_close
r3 = StepState.objects.filter(state_key='offer_ready_to_close')
if r3.count() < 1:
    new_3 = StepState(
        state_key = 'offer_ready_to_close',
        security_level = 0,
        group_key = 1,
        group_serial_number = 5,
        manual_set = False,
        is_alert_button = False
    )
    new_3.save()
    add_3 = StepState.objects.filter(state_key='offer_accepted').first()
    new_3.previous.add(add_3)
    new_3.save()
    t_en_3 = StepStateTranslation(
        state_name = "Ready to close offer",
        state_name_plural = "Ready to close offers",
        state_description = "ready to close offer",
        model = new_3,
        language = 'en'
    )
    t_en_3.save()
    t_de_3 = StepStateTranslation(
        state_name = "Zu schließen bereite Angebot",
        state_name_plural = "Zu schließen bereite Angebote",
        state_description = "zu schließen bereite angebot",
        model = new_3,
        language = 'de'
    )
    t_de_3.save()
    t_cs_3 = StepStateTranslation(
        state_name = "Nabídka připravená k uzavření",
        state_name_plural = "Nabídky připravené k uzavření",
        state_description = "nabídka připravená k uzavření",
        model = new_3,
        language = 'cs'
    )
    t_cs_3.save()

#----------------  offer_closed
r4 = StepState.objects.filter(state_key='offer_closed')
if r4.count() < 1:
    new_4 = StepState(
        state_key = 'offer_closed',
        security_level = 0,
        group_key = 1,
        group_serial_number = 6,
        manual_set = True,
        is_alert_button = False
    )
    new_4.save()
    add_4 = StepState.objects.filter(state_key='offer_ready_to_close').first()
    new_4.previous.add(add_4)
    new_4.save()
    t_en_4 = StepStateTranslation(
        state_name = "Closed offer",
        state_name_plural = "Closed offers",
        state_description = "closed offer",
        state_button_text = "Close Offer",
        state_template_title = "Offer closing",
        state_template_question = 'Are you sure, you want close offer',
        state_template_confitm_button = "Yes, Close",
        state_template_cancel_button = "Cancel",
        model = new_4,
        language = 'en'
    )
    t_en_4.save()
    t_de_4 = StepStateTranslation(
        state_name = "Geschlossenes Angebot",
        state_name_plural = "Geschlossene Angebote",
        state_description = "geschlossenes angebot",
        state_button_text = "Angebot schließen",
        state_template_title = "Angebot schließen",
        state_template_question = 'Sind Sie sicher, Sie wollen dem Angebot schließen',
        state_template_confitm_button = "Ja, schließen",
        state_template_cancel_button = "Stornieren",
        model = new_4,
        language = 'de'
    )
    t_de_4.save()
    t_cs_4 = StepStateTranslation(
        state_name = "Uzavřená nabídka",
        state_name_plural = "Uzavřené nabídky",
        state_description = "uzavřená nabídka",
        state_button_text = "Uzavřít nabídku",
        state_template_title = "Uzavření nabídky",
        state_template_question = 'Jste si jistý, že chete uzavřít nabídku',
        state_template_confitm_button = "Ano, zavřít",
        state_template_cancel_button = "Zrušit",
        model = new_4,
        language = 'cs'
    )
    t_cs_4.save()

#----------------  offer_canceled
r5 = StepState.objects.filter(state_key='offer_canceled')
if r5.count() < 1:
    new_5 = StepState(
        state_key = 'offer_canceled',
        security_level = 0,
        group_key = 1,
        group_serial_number = 7,
        manual_set = True,
        is_alert_button = True
    )
    new_5.save()
    add_5_1 = StepState.objects.filter(state_key='offer_new').first()
    new_5.previous.add(add_5_1)
    add_5_2 = StepState.objects.filter(state_key='offer_confirmed').first()
    new_5.previous.add(add_5_2)
    add_5_3 = StepState.objects.filter(state_key='offer_accepted').first()
    new_5.previous.add(add_5_3)
    add_5_4 = StepState.objects.filter(state_key='offer_ready_to_close').first()
    new_5.previous.add(add_5_4)
    add_5_5 = StepState.objects.filter(state_key='offer_in_auction').first()
    new_5.previous.add(add_5_5)
    new_5.save()
    t_en_5 = StepStateTranslation(
        state_name = "Canceled offer",
        state_name_plural = "Canceled offers",
        state_description = "canceled offer",
        state_button_text = "Cancel Offer",
        state_template_title = "Offer canceling",
        state_template_question = 'Are you sure, you want cancel offer',
        state_template_text = "If you cancel offer, you can't change it and you must contact poweruser.",
        state_template_confitm_button = "Yes, Cancel",
        state_template_cancel_button = "Do not cancel",
        model = new_5,
        language = 'en'
    )
    t_en_5.save()
    t_de_5 = StepStateTranslation(
        state_name = "Storniertes Angebot",
        state_name_plural = "Stornierte Angebote",
        state_description = "stornierte angebot",
        state_button_text = "Angebot stornieren",
        state_template_title = "Angebot stornieren",
        state_template_question = 'Sind Sie sicher, Sie wollen Angebot stornieren',
        state_template_text = "Wenn Sie das Angebot stornieren, können Sie es nicht ändern und Sie müssen poweruser Kontaktieren.",
        state_template_confitm_button = "Ja, stornieren",
        state_template_cancel_button = "Nicht stornieren",
        model = new_5,
        language = 'de'
    )
    t_de_5.save()
    t_cs_5 = StepStateTranslation(
        state_name = "Zrušená nabídka",
        state_name_plural = "Zrušené nabídka",
        state_description = "zrušená nabídka",
        state_button_text = "Zrušit nabídku",
        state_template_title = "Zrušení nabídky",
        state_template_question = 'Jste si jistý, že chete zrušit nabídku',
        state_template_text = "Když zrušíte nabídku, nemůžete jí dále měnit a musíte kontaktovat super uživatele.",
        state_template_confitm_button = "Ano, zrušit",
        state_template_cancel_button = "Nerušit",
        model = new_5,
        language = 'cs'
    )
    t_cs_5.save()

#========================================================

#----------------  answer_new
r6 = StepState.objects.filter(state_key='answer_new')
if r6.count() < 1:
    new_6 = StepState(
        state_key = 'answer_new',
        security_level = 0,
        group_key = 2,
        group_serial_number = 1,
        manual_set = False,
        is_alert_button = False
    )
    new_6.save()
    new_6.save()
    t_en_6 = StepStateTranslation(
        state_name = "New answer",
        state_name_plural = "New answers",
        state_description = "new answer",
        model = new_6,
        language = 'en'
    )
    t_en_6.save()
    t_de_6 = StepStateTranslation(
        state_name = "Neue Antwort",
        state_name_plural = "Neue Antworten",
        state_description = "neue antwort",
        model = new_6,
        language = 'de'
    )
    t_de_6.save()
    t_cs_6 = StepStateTranslation(
        state_name = "Nová odpověď",
        state_name_plural = "Nové odpověďi",
        state_description = "nová odpověď",
        model = new_6,
        language = 'cs'
    )
    t_cs_6.save()

#----------------  answer_confirmed
r7 = StepState.objects.filter(state_key='answer_confirmed')
if r7.count() < 1:
    new_7 = StepState(
        state_key = 'answer_confirmed',
        security_level = 0,
        group_key = 2,
        group_serial_number = 2,
        manual_set = True,
        is_alert_button = False,
    )
    new_7.save()
    add_7 = StepState.objects.filter(state_key='answer_new').first()
    new_7.previous.add(add_7)
    new_7.save()
    t_en_7 = StepStateTranslation(
        state_name = "Confirmed answer",
        state_name_plural = "Confirmed answers",
        state_description = "confirmed answer",
        state_button_text = "Confirm answer",
        state_template_title = "Answer confirmation",
        state_template_question = 'Are you sure, you want confirm answer',
        state_template_text = "If you confirm answer, you can't change it and you must contact poweruser.",
        state_template_confitm_button = "Yes, Confirm",
        state_template_cancel_button = "Cancel",
        model = new_7,
        language = 'en'
    )
    t_en_7.save()
    t_de_7 = StepStateTranslation(
        state_name = "Bestätigtes Antwort",
        state_name_plural = "Bestätigte Antworten",
        state_description = "bestätigte antwort",
        state_button_text = "Antwort bestätigen",
        state_template_title = "Antwort Bestätigung",
        state_template_question = 'Sind Sie sicher, Sie wollen das Antwort bestätigen',
        state_template_text = "Wenn Sie Antwort bestätigen, können Sie sie nicht ändern und Sie müssen poweruser Kontaktieren.",
        state_template_confitm_button = "Ja, Bestätigen",
        state_template_cancel_button = "Stornieren",
        model = new_7,
        language = 'de'
    )
    t_de_7.save()
    t_cs_7 = StepStateTranslation(
        state_name = "Potvrzená odpověď",
        state_name_plural = "Potvrzené odpověďi",
        state_description = "potvrzená odpověď",
        state_button_text = "Povtďte odpověď",
        state_template_title = "Potvrzení odpovědi",
        state_template_question = 'Jste si jistý, že chete potvrdit odpověď',
        state_template_text = "Když potvrdíte odpověď, nemůžete jí dále měnit a musíte kontaktovat super uživatele.",
        state_template_confitm_button = "Ano, potvrdit",
        state_template_cancel_button = "Zrušit",
        model = new_7,
        language = 'cs'
    )
    t_cs_7.save()

#----------------  answer_successful
r10 = StepState.objects.filter(state_key='answer_successful')
if r10.count() < 1:
    new_10 = StepState(
        state_key = 'answer_successful',
        security_level = 0,
        group_key = 2,
        group_serial_number = 3,
        manual_set = False,
        is_alert_button = False
    )
    new_10.save()
    add_10 = StepState.objects.filter(state_key='answer_confirmed').first()
    new_10.previous.add(add_10)
    new_10.save()
    t_en_10 = StepStateTranslation(
        state_name = "Successful answer",
        state_name_plural = "Successful answers",
        state_description = "successful answer",
        model = new_10,
        language = 'en'
    )
    t_en_10.save()
    t_de_10 = StepStateTranslation(
        state_name = "Erfolgreiches Antwort",
        state_name_plural = "Erfolgreiche Antworten",
        state_description = "erfolgreiche antwort",
        model = new_10,
        language = 'de'
    )
    t_de_10.save()
    t_cs_10 = StepStateTranslation(
        state_name = "Úspěšná odpověď",
        state_name_plural = "Úspěšné odpověďi",
        state_description = "úspěšná odpověď",
        model = new_10,
        language = 'cs'
    )
    t_cs_10.save()

#----------------  answer_accepted
r8 = StepState.objects.filter(state_key='answer_accepted')
if r8.count() < 1:
    new_8 = StepState(
        state_key = 'answer_accepted',
        security_level = 0,
        group_key = 2,
        group_serial_number = 4,
        manual_set = True,
        is_alert_button = False,
    )
    new_8.save()
    add_8 = StepState.objects.filter(state_key='answer_successful').first()
    new_8.previous.add(add_8)
    new_8.save()
    t_en_8 = StepStateTranslation(
        state_name = "Accepted answer",
        state_name_plural = "Accepted answers",
        state_description = "accepted answer",
        state_button_text = "Accept answer",
        state_template_title = "Accept answer",
        state_template_question = 'Are you sure, you want accept successful answer',
        state_template_confitm_button = "Yes, Accept",
        state_template_cancel_button = "Cancel",
        model = new_8,
        language = 'en'
    )
    t_en_8.save()
    t_de_8 = StepStateTranslation(
        state_name = "Akzeptiertes Antwort",
        state_name_plural = "Akzeptierte Antworten",
        state_description = "akzeptierte antwort",
        state_button_text = "Antwort akzeptieren",
        state_template_title = "Antwort akzeptieren",
        state_template_question = 'Sind Sie sicher, Sie wollen erfolgreiche Antwort annehmen',
        state_template_confitm_button = "Ja, Akzeptier",
        state_template_cancel_button = "Stornieren",
        model = new_8,
        language = 'de'
    )
    t_de_8.save()
    t_cs_8 = StepStateTranslation(
        state_name = "Přijatá odpověď",
        state_name_plural = "Přijaté odpověďi",
        state_description = "přijatá odpověď",
        state_button_text = "Přijmout odpověď",
        state_template_title = "Přijmout odpověď",
        state_template_question = 'Jste si jistý, že chete přijmout úspěšnou odpověď',
        state_template_confitm_button = "Ano, přimout",
        state_template_cancel_button = "Zrušit",
        model = new_8,
        language = 'cs'
    )
    t_cs_8.save()

#----------------  answer_closed
r8 = StepState.objects.filter(state_key='answer_closed')
if r8.count() < 1:
    new_8 = StepState(
        state_key = 'answer_closed',
        security_level = 0,
        group_key = 2,
        group_serial_number = 5,
        manual_set = True,
        is_alert_button = False,
    )
    new_8.save()
    add_8 = StepState.objects.filter(state_key='answer_accepted').first()
    new_8.previous.add(add_8)
    new_8.save()
    t_en_8 = StepStateTranslation(
        state_name = "Closed answer",
        state_name_plural = "Closed answers",
        state_description = "closed answer",
        state_button_text = "Close answer",
        state_template_title = "Answer closing",
        state_template_question = 'Are you sure, you want close answer',
        state_template_confitm_button = "Yes, Close",
        state_template_cancel_button = "Cancel",
        model = new_8,
        language = 'en'
    )
    t_en_8.save()
    t_de_8 = StepStateTranslation(
        state_name = "Geschlossenes Antwort",
        state_name_plural = "Geschlossene Antworten",
        state_description = "geschlossene antwort",
        state_button_text = "Antwort schließen",
        state_template_title = "Antwort schließen",
        state_template_question = 'Sind Sie sicher, Sie wollen die Antwort schließen',
        state_template_confitm_button = "Ja, schließen",
        state_template_cancel_button = "Stornieren",
        model = new_8,
        language = 'de',
    )
    t_de_8.save()
    t_cs_8 = StepStateTranslation(
        state_name = "Uzavřená odpověď",
        state_name_plural = "Uzavřené odpověďi",
        state_description = "uzavřená odpověď",
        state_button_text = "Uzavřít odpověď",
        state_template_title = "Uzavřít odpověď",
        state_template_question = 'Jste si jistý, že chete zavřít odpověď',
        state_template_confitm_button = "Ano, zavřít",
        state_template_cancel_button = "Zrušit",
        model = new_8,
        language = 'cs'
    )
    t_cs_8.save()

#----------------  answer_canceled
r9 = StepState.objects.filter(state_key='answer_canceled')
if r9.count() < 1:
    new_9 = StepState(
        state_key = 'answer_canceled',
        security_level = 0,
        group_key = 2,
        group_serial_number = 6,
        manual_set = True,
        is_alert_button = True
    )
    new_9.save()
    add_9_1 = StepState.objects.filter(state_key='answer_new').first()
    new_9.previous.add(add_9_1)
    add_9_2 = StepState.objects.filter(state_key='answer_confirmed').first()
    new_9.previous.add(add_9_2)
    add_9_3 = StepState.objects.filter(state_key='answer_successful').first()
    new_9.previous.add(add_9_3)
    add_9_4 = StepState.objects.filter(state_key='answer_accepted').first()
    new_9.previous.add(add_9_4)
    new_9.save()
    t_en_9 = StepStateTranslation(
        state_name = "Canceled answer",
        state_name_plural = "Canceled answers",
        state_description = "canceled answer",
        state_button_text = "Cancel Answer",
        state_template_title = "Answer canceling",
        state_template_question = 'Are you sure, you want cancel answer',
        state_template_text = "If you cancel answer, you can't change it and you must contact poweruser.",
        state_template_confitm_button = "Yes, Cancel",
        state_template_cancel_button = "Do not cancel",
        model = new_9,
        language = 'en'
    )
    t_en_9.save()
    t_de_9 = StepStateTranslation(
        state_name = "Storniertes Antwort",
        state_name_plural = "Stornierte Antworten",
        state_description = "stornierte antwort",
        state_button_text = "Antwort stornieren",
        state_template_title = "Antwort  stornieren",
        state_template_question = 'Sind Sie sicher, Sie wollen Antwort stornieren',
        state_template_text = "Wenn Sie das Antwort stornieren, können Sie es nicht ändern und Sie müssen poweruser Kontaktieren.",
        state_template_confitm_button = "Ja, stornieren",
        state_template_cancel_button = "Nicht stornieren",
        model = new_9,
        language = 'de'
    )
    t_de_9.save()
    t_cs_9 = StepStateTranslation(
        state_name = "Zrušená odpověď",
        state_name_plural = "Zrušené odpověďi",
        state_description = "zrušená odpověď",
        state_button_text = "Zrušit odpověď",
        state_template_title = "Zrušení odpověďi",
        state_template_question = 'Jste si jistý, že chete zrušit odpověď',
        state_template_text = "Když zrušíte odpověď, nemůžete jí dále měnit a musíte kontaktovat super uživatele.",
        state_template_confitm_button = "Ano, zrušit",
        state_template_cancel_button = "Nerušit",
        model = new_9,
        language = 'cs',
    )
    t_cs_9.save()
