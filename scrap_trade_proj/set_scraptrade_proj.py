from project_main.models import Project, StaticPage, StaticPageTranslation

f1 = Project.objects.filter(project_name = 'scraptrade')
if f1.count() > 0:
    proj = f1.first()
else:
    proj = Project(
        project_name = 'scraptrade',
        project_description = 'Burza odpadovych surovin',
    )
    proj.save()

r0 = StaticPage.objects.filter(page_code='project-home')
if r0.count() < 1:
    new_0 = StaticPage(
        page_code = 'project-home',
        sequence = 0,
        project = proj,
    )
    new_0.save()
    t_en_0 = StaticPageTranslation(
        page_name = 'Home',
        page_title = """
            <h1>Every waste</h1>
            <h1>HAS ITS VALUE</h1>
        """,
        page_body = "",
        model = new_0,
        language = 'en',
    )
    t_en_0.save()
    t_de_0 = StaticPageTranslation(
        page_name = 'Home',
        page_title = """
            <h1>Jeder Abfall</h1>
            <h1>HAT SEINEM WERT</h1>
        """,
        page_body = "",
        model = new_0,
        language = 'de',
    )
    t_de_0.save()
    t_cs_0 = StaticPageTranslation(
        page_name = 'Domácí strana',
        page_title = """
            <h1>Každý odpad</h1>
            <h1>MÁ SVOJÍ HODNOTU</h1>
        """,
        page_body = "",
        model = new_0,
        language = 'cs',
    )
    t_cs_0.save()


r1 = StaticPage.objects.filter(page_code='who_are_we')
if r1.count() < 1:
    new_1 = StaticPage(
        page_code = 'who_are_we',
        sequence = 1,
        project = proj,
    )
    new_1.save()
    t_en_1 = StaticPageTranslation(
        page_name = 'WHO ARE WE',
        page_title = "<h1>Who are we</h1>",
        page_body = """
            <div class= "stat_page_body">
                <p>A unique project in the Czech Republic with a focus on waste trading.</p>
                <p>We use modern technologies and innovative tools for a wide and creative range of uses.</p>
            </div>
        """,
        model = new_1,
        language = 'en',
    )
    t_en_1.save()
    t_de_1 = StaticPageTranslation(
        page_name = 'WER SIND WIR',
        page_title = "<h1>Wer sind wir</h1>",
        page_body = """
            <div class= "stat_page_body">
                <p>Ein einzigartiges Projekt in der Tschechischen Republik mit Schwerpunkt im abfallhandel.</p>
                <p>Wir verwenden moderne Technologien und innovative Werkzeuge für ein breites und kreatives Einsatzspektrum.</p>
            </div>
        """,
        model = new_1,
        language = 'de',
    )
    t_de_1.save()
    t_cs_1 = StaticPageTranslation(
        page_name = 'KDO JSME',
        page_title = "<h1>Kdo jsme</h1>",
        page_body = """
            <div class="stat_page_body">
                <p>Unikátní projekt v České republice se zaměřením na obchodování s odpady.</p>
                <p>Využíváme moderní technologie, inovativní nástroje pro široké a kreativní spektrum využití.</p>
            </div>
        """,
        model = new_1,
        language = 'cs',
    )
    t_cs_1.save()

r2 = StaticPage.objects.filter(page_code='how_we_work')
if r2.count() < 1:
    new_2 = StaticPage(
        page_code = 'how_we_work',
        sequence = 2,
        project = proj,
    )
    new_2.save()
    t_en_2 = StaticPageTranslation(
        page_name = 'HOW WE WORK',
        page_title = "<h1>How we work</h1>",
        page_body = """
            <div>
                <p>ScrapTrade creates a circular economy based on secondary raw materials as sources. This system stands on three basic pillars.</p>
                <p></p>
                <p> I. Legislation - we are based on the legislation in force. We will deliver relevant information directly to the consumer.</p>
                <p></p>
                <p> II. Trading platform - we use market mechanisms to combine producers and final processors.</p>
                <p></p>
                <P> III. Waste management - we map the movement of waste production and processing on the basis of trading activity according to Government Regulation No. 352/2014 Sb.</p>
            </div>
        """,
        model = new_2,
        language = 'en',
    )
    t_en_2.save()
    t_de_2 = StaticPageTranslation(
        page_name = 'WIE WIR ARBEITEN',
        page_title = "<h1>Wie wir arbeiten</h1>",
        page_body = """
            <div>
                <p>ScrapTrade schafft eine Kreislaufwirtschaft, die auf sekundären Rohstoffen als Quellen basiert. Dieses system steht auf drei Grundpfeilern.</p>
                <p></p>
                <p> I. Gesetzgebung - wir basieren auf den geltenden Rechtsvorschriften. Wir liefern relevante Informationen direkt an den Verbraucher.</p>
                <p></p>
                <p> II. Handelsplattform - wir nutzen Marktmechanismen, um Produzenten und endverarbeiter zu kombinieren.</p>
                <p></p>
                <p> III. Abfallwirtschaft-wir ordnen die Bewegung der Abfallproduktion und-Verarbeitung auf der Grundlage der Handelsaktivität gemäß Der Regierungsverordnung Nr. 352/2014 Sb.</p>
            </div>
        """,
        model = new_2,
        language = 'de',
    )
    t_de_2.save()
    t_cs_2 = StaticPageTranslation(
        page_name = 'JAK FUNGUJEME',
        page_title = "<h1>Jak fungujeme</h1>",
        page_body = """
            <div>
                <p>ScrapTrade vytváří oběhové hospodářství založené na druhotných surovinách jako zdrojích. Tento systém stojí na třech základních pilířích.</p>
             <p></p>
                <p>I. Legislativa - vycházíme z platné legislativy. Doručíme relevantní informace přímo ke spotřebiteli.</p>

            <p></p>
              <p>II. Obchodní platforma - využíváme tržní mechanismy ke spojení producentů a finálních zpracovatelů.</p>
            <p></p>
              <p>III. Odpadové hospodářství - mapujeme pohyb produkce a zpracování odpadů na základě aktivity obchodování dle nařízení vlády č. 352/2014 Sb.</p>
            </div>
        """,
        model = new_2,
        language = 'cs',
    )
    t_cs_2.save()

r3 = StaticPage.objects.filter(page_code='partners')
if r3.count() < 1:
    new_3 = StaticPage(
        page_code = 'partners',
        sequence = 3,
        project = proj,
    )
    new_3.save()
    t_en_3 = StaticPageTranslation(
        page_name = 'PARTNERS',
        page_title = "<h1>Partners</h1>",
        page_body = "",
        model = new_3,
        language = 'en',
    )
    t_en_3.save()
    t_de_3 = StaticPageTranslation(
        page_name = 'PARTNER',
        page_title = "<h1>Partner</h1>",
        page_body = "",
        model = new_3,
        language = 'de',
    )
    t_de_3.save()
    t_cs_3 = StaticPageTranslation(
        page_name = 'PARTNEŘI',
        page_title = "<h1>Partneři</h1>",
        page_body = "",
        model = new_3,
        language = 'cs',
    )
    t_cs_3.save()

r4 = StaticPage.objects.filter(page_code='contacts')
if r4.count() < 1:
    new_4 = StaticPage(
        page_code = 'contacts',
        sequence = 4,
        project = proj,
    )
    new_4.save()
    t_en_4 = StaticPageTranslation(
        page_name = 'CONTACTS',
        page_title = "<h1>Contacts:</h1>",
        page_body = """
            <div>
              <p/>
              <h3>Scrap Trade s. r. o.</h3>
              <P>Kamenný Újezd 179, Nýřany</p>
              <p/>
              <h5>phone</h5>
              <p>+420 608 155 552</p>
              <p/>
              <h5>e-mail</h5>
              <p>info@scraptrade.cz</p>
              <p/>
              <h5>ID, registration</h5>
              <p>04635523, s. Z. C32047 Regional Court Pilsen</p>
            </div>
        """,
        model = new_4,
        language = 'en',
    )
    t_en_4.save()
    t_de_4 = StaticPageTranslation(
        page_name = 'KONTAKTE',
        page_title = "<h1>Kontakte:</h1>",
        page_body = """
            <div>
              <p/>
              <h3>Scrap Trade s. r. o..</h3>
              <P>Kamenný Újezd 179, Nýřany</p>
              <p/>
              <h5> Telefon</h5>
              <p>+420 608 155 552</p>
              <p/>
              <h5>e-mail</h5>
              <p>info@scraptrade.cz</p>
              <p/>
              <h5> ID, Registrierung</h5>
              <p> 04635523, s. Z. C32047 Landgericht Pilsen</p>
            </div>
        """,
        model = new_4,
        language = 'de',
    )
    t_de_4.save()
    t_cs_4 = StaticPageTranslation(
        page_name = 'KONTAKT',
        page_title = "<h1>Kontakt:</h1>",
        page_body = """
            <div>
              <p/>
              <h3>Scrap Trade s.r.o.</h3>
              <p>Kamenný Újezd 179, Nýřany</p>
              <p/>
              <h5>telefon</h5>
              <p>+420 608 155 552</p>
              <p/>
              <h5>e-mail</h5>
              <p>info@scraptrade.cz</p>
              <p/>
              <h5>ičo, registrace</h5>
              <p>04635523, s.z. C32047 Krajský soudu Plzeň</p>
            </div>
        """,
        model = new_4,
        language = 'cs',
    )
    t_cs_4.save()
