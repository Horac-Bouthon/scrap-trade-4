from notification.models import MessTemp, MessTempTranslation
from state_wf.models import StepState

#-----------------  fallback
r0 = MessTemp.objects.filter(temp_key='fallback')
if r0.count() < 1:
    new_0 = MessTemp(
        temp_key = 'fallback',
        temp_type = 'text',
    )
    new_0.save()
    m_st = """\
This message is automatically generated, please do not reply to it.

Dear customer,

we're so sorry.
This is a test message and was sent by mistake.
We will try not to repeat anything like this.
Thank you for your leniency and wish you a successful day.

Your Team
"""
    t_en_0 = MessTempTranslation(
        subject = "noreply({{ app_name }}): replacement message",
        body = m_st,
        model = new_0,
        language = 'en',
    )
    t_en_0.save()
    m_st = """\
Diese Nachricht wird automatisch generiert, bitte Antworten Sie nicht darauf.

Sehr geehrte Kunde,

wir bitten um Enschuldigung.
Dies ist eine testmeldung und wurde versehentlich gesendet.
Wir werden versuchen, so etwas nicht zu wiederholen.
Vielen Dank für Ihre Nachsicht und wir wünschen Ihnen einen erfolgreichen Tag.

Ihr Team
"""
    t_de_0 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Ersatz-Nachricht",
        body = m_st,
        model = new_0,
        language = 'de',
    )
    t_de_0.save()
    m_st = """\
Tato zpráva je automaticky generovaná, prosím, neodpovídejte na ni.

Vážený zákazníku,

moc se omlouváme.
Jedná se o testovací zprávu a byla odeslána nedopatřením.
Budeme se snažit, aby se nic podobného neopakovalo.
Děkujeme za shovívavost a přejeme úspěšný den.

Váš Team
"""
    t_cs_0 = MessTempTranslation(
        subject = "noreply({{ app_name }}): náhradní zpráva",
        body = m_st,
        model = new_0,
        language = 'cs'
    )
    t_cs_0.save()

#-----------------  ntf_failur
r1 = MessTemp.objects.filter(temp_key='ntf_failur')
if r1.count() < 1:
    new_1 = MessTemp(
        temp_key = 'ntf_failur',
        temp_type = 'html',
    )
    new_1.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <h1>Can't send email</h1>
    <div>
      <h3>Parameters</h3>
      <table>
        <tr>
          <td><b>Place</b></td>
          <td>{{ place }}</td>
        </tr>
        <tr>
          <td><b>URL</b></td>
          <td>{{ url }}</td>
        </tr>
        <tr>
          <td><b>User</b></td>
          <td>{{ user_mail }} ({{ user_cust }})</td>
        </tr>
      </table>
    </div>
    <div>
      <h3>Original message</h3>
      <div>
      {{ orig|safe }}
      </div>
    </div>
  </body>
</html>
"""
    t_en_1 = MessTempTranslation(
        subject = "noreply({{ app_name }}): nft failure",
        body = m_st,
        model = new_1,
        language = 'en',
    )
    t_en_1.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <h1>Kann nicht einem E-Mail senden</h1>
    <div>
      <h3>Parameter</h3>
      <table>
        <tr>
          <td><b>Ort</b></td>
          <td>{{ place }}</td>
        </tr>
        <tr>
          <td><b>URL</b></td>
          <td>{{ url }}</td>
        </tr>
        <tr>
          <td><b>Benutzer</b></td>
          <td>{{ user_mail }} ({{ user_cust }})</td>
        </tr>
      </table>
    </div>
    <div>
      <h3>Ursprüngliche Nachricht</h3>
      <div>
      {{ orig|safe }}
      </div>
    </div>
  </body>
</html>
"""
    t_de_1 = MessTempTranslation(
        subject = "noreply({{ app_name }}): nft Fehler",
        body = m_st,
        model = new_1,
        language = 'de',
    )
    t_de_1.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <h1>Nemohu odeslat E-Mail</h1>
    <div>
      <h3>Parametry</h3>
      <table>
        <tr>
          <td><b>Místo</b></td>
          <td>{{ place }}</td>
        </tr>
        <tr>
          <td><b>URL</b></td>
          <td>{{ url }}</td>
        </tr>
        <tr>
          <td><b>Uživatel</b></td>
          <td>{{ user_mail }} ({{ user_cust }})</td>
        </tr>
      </table>
    </div>
    <div>
      <h3>Původní zpráva</h3>
      <div>
      {{ orig|safe }}
      </div>
    </div>
  </body>
</html>
"""
    t_cs_1 = MessTempTranslation(
        subject = "noreply({{ app_name }}): chyba ntf",
        body = m_st,
        model = new_1,
        language = 'cs'
    )
    t_cs_1.save()

#-----------------  offer_publicate
r2 = MessTemp.objects.filter(temp_key='offer_publicate')
if r2.count() < 1:
    new_2 = MessTemp(
        temp_key = 'offer_publicate',
        temp_type = 'html',
    )
    new_2.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>A new offer has been assigned to you</h1>
    <div>
      You can reply to the offer at: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Detail</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Required minimum price:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Delivery date:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_2 = MessTempTranslation(
        subject = "noreply({{ app_name }}): new offer has been assigned to you",
        body = m_st,
        model = new_2,
        language = 'en',
    )
    t_en_2.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Sie haben ein neues Angebot erhalten</h1>
    <div>
      Sie können das Angebot beantworten unter: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Detail</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Mindestpreis:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Liefertermin:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_2 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Sie haben ein neues Angebot erhalten",
        body = m_st,
        model = new_2,
        language = 'de',
    )
    t_de_2.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
    <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
    </div>
    <br>
    <h1>Byla vám přiřazena nová nabídka</h1>
    <div>
      Můžete na nabídku odpovědět na adrese: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
   <br>
    <div>
      <h2>Podrobnosti</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Minimální požadovaná cena:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Datum dodání:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_2 = MessTempTranslation(
        subject = "noreply({{ app_name }}): byla vám přiřazena nová nabídka",
        body = m_st,
        model = new_2,
        language = 'cs'
    )
    t_cs_2.save()

    state = StepState.objects.filter(state_key = 'offer_confirmed').first()
    state.send_ntf = True
    state.ntf_template = new_2
    state.save()

#-----------------  report_success
r3 = MessTemp.objects.filter(temp_key='report_success')
if r3.count() < 1:
    new_3 = MessTemp(
        temp_key = 'report_success',
        temp_type = 'html',
    )
    new_3.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>Your answer won the {{ item.ah_offer.description }} auction</h1>
    <div>
      You can confirm the result at: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Your answer</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Total price offered:</b> {{ item.total_price }}
        </p>
      </div>
    </div>
    <br>
    <div>
      <h2>Offer</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Required minimum price:</b> {{ item.ah_offer.minimal_total_price }}
        </p>
        <p>
          <b>Delivery date:</b> {{ item.ah_offer.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_3 = MessTempTranslation(
        subject = "noreply({{ app_name }}): your answer was sucessful",
        body = m_st,
        model = new_3,
        language = 'en',
    )
    t_en_3.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Ihr Gebot gewann die {{ item.ah_offer.description }} Auktion</h1>
    <div>
      Sie können das Ergebnis auf <a href="{{ access_url }}">{{ access_url }}</a> bestätigen.
    </div>
    <br>
    <div>
      <h2>Ihre Antwort</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Gesamtpreis angeboten:</b> {{ item.total_price }}
        </p>
      </div>
    </div>
    <br>
    <div>
      <h2>Angebot</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Mindestpreis:</b> {{ item.ah_offer.minimal_total_price }}
        </p>
        <p>
          <b>Liefertermin:</b> {{ item.ah_offer.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_3 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Ihre Antwort war erfolgreich",
        body = m_st,
        model = new_3,
        language = 'de',
    )
    t_de_3.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>Vaše odpověď vyhrála aukci {{ item.ah_offer.description }}</h1>
     <div>
      Výsledek můžete potvrdit na adrese: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Vaše odpověď</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Nabídnutá cena celkem:</b> {{ item.total_price }}
        </p>
      </div>
    </div>
    <br>
    <div>
      <h2>Nabídka</h2>
      <div>
        <h3>{{ item.ah_offer.description }}</h3>
        <p>
          <b>Minimální požadovaná cena:</b> {{ item.ah_offer.minimal_total_price }}
        </p>
        <p>
          <b>Datum dodání:</b> {{ item.ah_offer.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_3 = MessTempTranslation(
        subject = "noreply({{ app_name }}): vaše odpověď byla úspěšná",
        body = m_st,
        model = new_3,
        language = 'cs'
    )
    t_cs_3.save()

    state = StepState.objects.filter(state_key = 'answer_successful').first()
    state.send_ntf = True
    state.ntf_template = new_3
    state.save()

#-----------------  offer_accepted
r4 = MessTemp.objects.filter(temp_key='offer_accepted')
if r4.count() < 1:
    new_4 = MessTemp(
        temp_key = 'offer_accepted',
        temp_type = 'html',
    )
    new_4.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>Your offer {{ item.description }} was auctioned</h1>
    <div>
      See the details at: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Offer</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Required minimum price:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Delivery date:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_4 = MessTempTranslation(
        subject = "noreply({{ app_name }}): your offer was sucessful",
        body = m_st,
        model = new_4,
        language = 'en',
    )
    t_en_4.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Ihr Angebot {{ item.description }} wurde versteigert</h1>
    <div>
      Siehe die details unter <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Angebot</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Mindestpreis:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Liefertermin:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_4 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Ihr Angebot war erfolgreich",
        body = m_st,
        model = new_4,
        language = 'de',
    )
    t_de_4.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>Vaše nabidka {{ item.description }} byla vydražena</h1>
     <div>
      Podrobnosti si prohlédněta na adrese: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Nabídka</h2>
      <div>
        <h3>{{ item.ah_offer.description }}</h3>
        <p>
          <b>Minimální požadovaná cena:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Datum dodání:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_4 = MessTempTranslation(
        subject = "noreply({{ app_name }}): vaše nabídka byla úspěšná",
        body = m_st,
        model = new_4,
        language = 'cs'
    )
    t_cs_4.save()

    state = StepState.objects.filter(state_key = 'offer_accepted').first()
    state.send_ntf = True
    state.ntf_template = new_4
    state.save()

#-----------------  offer_ready_to_close
r5 = MessTemp.objects.filter(temp_key='offer_ready_to_close')
if r5.count() < 1:
    new_5 = MessTemp(
        temp_key = 'offer_ready_to_close',
        temp_type = 'html',
    )
    new_5.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>For offer {{ item.description }} partner closed reply</h1>
    <div>
      Check offer and close it: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Offer</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Required minimum price:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Delivery date:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_5 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Your offer is ready for closure",
        body = m_st,
        model = new_5,
        language = 'en',
    )
    t_en_5.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Für dem Angebot {{ item.Beschreibung }} hat der Partner die Antwort geschlossen</h1>
    <div>
      Überprüfen Sie das Angebot und schließen Sie es: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Angebot</h2>
      <div>
        <h3>{{ item.description }}</h3>
        <p>
          <b>Mindestpreis:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Liefertermin:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_5 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Ihr Angebot ist zum Abschluss bereit",
        body = m_st,
        model = new_5,
        language = 'de',
    )
    t_de_5.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>U nabídky {{ item.description }} partner uzavřel odpověď</h1>
     <div>
      Překontrolujte nabídku a uzavřete ji: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <h2>Nabídka</h2>
      <div>
        <h3>{{ item.ah_offer.description }}</h5>
        <p>
          <b>Minimální požadovaná cena:</b> {{ item.minimal_total_price }}
        </p>
        <p>
          <b>Datum dodání:</b> {{ item.delivery_date|date:"d.m.Y" }}
        </p>
      </div>
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_5 = MessTempTranslation(
        subject = "noreply({{ app_name }}): vaše nabídka je připravena k uzavření",
        body = m_st,
        model = new_5,
        language = 'cs'
    )
    t_cs_5.save()

    state = StepState.objects.filter(state_key = 'offer_ready_to_close').first()
    state.send_ntf = True
    state.ntf_template = new_5
    state.save()

#-----------------  auction_ended
r6 = MessTemp.objects.filter(temp_key='auction_ended')
if r6.count() < 1:
    new_6 = MessTemp(
        temp_key = 'auction_ended',
        temp_type = 'html',
    )
    new_6.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>The auction of {{ offer_description }} ended</h1>
    <br>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_6 = MessTempTranslation(
        subject = "noreply({{ app_name }}): The auction of {{ offer_description }} ended",
        body = m_st,
        model = new_6,
        language = 'en',
    )
    t_en_6.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Die Auktion für {{offer_description }} wurde beendet</h1>
    <br>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_6 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Die Auktion für {{ offer_description }} wurde beendet",
        body = m_st,
        model = new_6,
        language = 'de',
    )
    t_de_6.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>Aukce {{ offer_description }} byla ukončena</h1>
     <br>
   <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_6 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Aukce {{ offer_description }} byla ukončena",
        body = m_st,
        model = new_6,
        language = 'cs'
    )
    t_cs_6.save()

#-----------------  offer_no_answers
r7 = MessTemp.objects.filter(temp_key='offer_no_answers')
if r7.count() < 1:
    new_7 = MessTemp(
        temp_key = 'offer_no_answers',
        temp_type = 'html',
    )
    new_7.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>Offer {{ item.description }} has been cancelled</h1>
    <br>
    <div>
      No one showed any interest and sent a response.
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_7 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Your offer {{ item.description }} has been cancelled",
        body = m_st,
        model = new_7,
        language = 'en',
    )
    t_en_7.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Angebot {{offer_description }} wurde abgebrochen</h1>
    <br>
    <div>
      Niemand zeigte Interesse und schickte eine Antwort.
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_7 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Ihr Angebot {{offer_description }} wurde abgebrochen",
        body = m_st,
        model = new_7,
        language = 'de',
    )
    t_de_7.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>Nabídka {{ offer_description }} byla zrušena</h1>
    <br>
     <div>
      Nikdo neprojevil zájem a neposlal odpověď.
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_7 = MessTempTranslation(
        subject = "noreply({{ app_name }}): vaše nabídka {{ offer_description }} byla zrušena",
        body = m_st,
        model = new_7,
        language = 'cs'
    )
    t_cs_7.save()

#-----------------  set_password
r8 = MessTemp.objects.filter(temp_key='set_password')
if r8.count() < 1:
    new_8 = MessTemp(
        temp_key = 'set_password',
        temp_type = 'html',
    )
    new_8.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}.</small>
    </div>
    <br>
    <h1>Reset password</h1>
    <div>
      Reset link: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_8 = MessTempTranslation(
        subject = "({{ app_name }}): Reset user password",
        body = m_st,
        model = new_8,
        language = 'en',
    )
    t_en_8.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert.</small>
    </div>
    <br>
    <h1>Passwort zurücksetzen</h1>
    <div>
      Reset-link: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_8 = MessTempTranslation(
        subject = "({{ app_name }}): Passwort zurücksetzen",
        body = m_st,
        model = new_8,
        language = 'de',
    )
    t_de_8.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
     <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}.</small>
     </div>
     <br>
     <h1>Nastavit heslo</h1>
    <div>
      Odkaz na nastavení: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_8 = MessTempTranslation(
        subject = "({{ app_name }}): nastavit uživatelské heslo",
        body = m_st,
        model = new_8,
        language = 'cs'
    )
    t_cs_8.save()

#-----------------  auction_started
r9 = MessTemp.objects.filter(temp_key='auction_started')
if r9.count() < 1:
    new_9 = MessTemp(
        temp_key = 'auction_started',
        temp_type = 'html',
    )
    new_9.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>This message was automatically generated by the application {{ app_name }}. Do not response.</small>
    </div>
    <br>
    <h1>The auction of {{ offer_description }} started</h1>
    <div>
      Online auction: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <p>Excuse the interruption and have a nice day.</p>
      <p>Your Team</p>
    </div>
  </body>
</html>
"""
    t_en_9 = MessTempTranslation(
        subject = "noreply({{ app_name }}): The auction of {{ offer_description }} started",
        body = m_st,
        model = new_9,
        language = 'en',
    )
    t_en_9.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
     <small>Diese Nachricht wurde automatisch von der Anwendung {{ app_name }} generiert. Nicht Antworten.</small>
    </div>
    <br>
    <h1>Die Auktion für {{offer_description }} hat begonnent</h1>
    <div>
      Online-Auktion: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <p>Entschuldigen Sie die Unterbrechung und wir wünschen euch einen schönen Tag.</p>
      <p>Ihr Team</p>
    </div>
  </body>
</html>
"""
    t_de_9 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Die Auktion für {{ offer_description }} hat begonnen",
        body = m_st,
        model = new_9,
        language = 'de',
    )
    t_de_9.save()
    m_st = """\
<!DOCTYPE html>
<html>
  <body>
    <div>
      <small>Tato zpráva byla automaticky vygenerována aplikaci {{ app_name }}. Neodpovídejte na ni.</small>
     </div>
     <br>
     <h1>Aukce {{ offer_description }} začala</h1>
    <div>
      Online aukce: <a href="{{ access_url }}">{{ access_url }}</a>
    </div>
    <br>
    <div>
      <p>Omlouváme se za vyrušení a přejeme hezký den.</p>
      <p>Váš tým</p>
    </div>
  </body>
</html>
"""
    t_cs_9 = MessTempTranslation(
        subject = "noreply({{ app_name }}): Aukce {{ offer_description }} byla zahájena",
        body = m_st,
        model = new_9,
        language = 'cs'
    )
    t_cs_9.save()
