from doc_repo.models import DocType, DocTypeTranslation

#----------------  picture
r0 = DocType.objects.filter(type_key='picture')
if r0.count() < 1:
    new_0 = DocType(
        type_key = 'picture',
    )
    new_0.save()
    t_en_0 = DocTypeTranslation(
        type_name = "picture",
        model = new_0,
        language = 'en'
    )
    t_en_0.save()
    t_de_0 = DocTypeTranslation(
        type_name = "Bild",
        model = new_0,
        language = 'de',
    )
    t_de_0.save()
    t_cs_0 = DocTypeTranslation(
        type_name = "obrázek",
        model = new_0,
        language = 'cs'
    )
    t_cs_0.save()

#----------------  pdf
r1 = DocType.objects.filter(type_key='pdf')
if r1.count() < 1:
    new_1 = DocType(
        type_key = 'pdf',
    )
    new_1.save()
    new_1.save()
    t_en_1 = DocTypeTranslation(
        type_name = "pdf",
        model = new_1,
        language = 'en'
    )
    t_en_1.save()
    t_de_1 = DocTypeTranslation(
        type_name = "Pdf",
        model = new_1,
        language = 'de',
    )
    t_de_1.save()
    t_cs_1 = DocTypeTranslation(
        type_name = "pdf",
        model = new_1,
        language = 'cs'
    )
    t_cs_1.save()

#----------------  file
r2 = DocType.objects.filter(type_key='file')
if r2.count() < 1:
    new_2 = DocType(
        type_key = 'file',
    )
    new_2.save()
    t_en_2 = DocTypeTranslation(
        type_name = "file",
        model = new_2,
        language = 'en'
    )
    t_en_2.save()
    t_de_2 = DocTypeTranslation(
        type_name = "Datei",
        model = new_2,
        language = 'de',
    )
    t_de_2.save()
    t_cs_2 = DocTypeTranslation(
        type_name = "soubor",
        model = new_2,
        language = 'cs'
    )
    t_cs_2.save()
