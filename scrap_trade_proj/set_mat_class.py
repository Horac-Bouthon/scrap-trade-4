from auction_house.models import (
    AhMatClass,
    AhMatClassTranslation,
)

mcs = AhMatClass.objects.filter(class_name = 'Material class 1')
if mcs.count() > 0:
    mc = mcs.first()
else:
    mc = AhMatClass(
        class_name = 'Material class 1',
        measurement_unit = 'm2'
    )
    mc.save()

mcs_en = mc.translations.filter(language = 'en')
if mcs_en.count() > 0:
    mc_en = mcs_en.first()
else:
    mc_en = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'en',
    )
mc_en.display_name = 'Material class 1'
mc_en.mat_class_description = 'something in square meters'
mc_en.save()

mcs_de = mc.translations.filter(language = 'de')
if mcs_de.count() > 0:
    mc_de = mcs_de.first()
else:
    mc_de = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'de',
    )
mc_de.display_name = 'Materialklasse 1'
mc_de.mat_class_description = 'etwas in Quadratmetern'
mc_de.save()

mcs_cs = mc.translations.filter(language = 'cs')
if mcs_cs.count() > 0:
    mc_cs = mcs_cs.first()
else:
    mc_cs = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'cs',
    )
mc_cs.display_name = 'Třída materiálu 1'
mc_cs.mat_class_description = 'něco ve čverečnich metrech'
mc_cs.save()

#----------------------------------------------------------------

mcs = AhMatClass.objects.filter(class_name = 'Material class 2')
if mcs.count() > 0:
    mc = mcs.first()
else:
    mc = AhMatClass(
        class_name = 'Material class 2',
        measurement_unit = 'T'
    )
    mc.save()

mcs_en = mc.translations.filter(language = 'en')
if mcs_en.count() > 0:
    mc_en = mcs_en.first()
else:
    mc_en = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'en',
    )
mc_en.display_name = 'Material class 2'
mc_en.mat_class_description = 'something in tonnes'
mc_en.save()

mcs_de = mc.translations.filter(language = 'de')
if mcs_de.count() > 0:
    mc_de = mcs_de.first()
else:
    mc_de = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'de',
    )
mc_de.display_name = 'Materialklasse 2'
mc_de.mat_class_description = 'etwas in Tonnen'
mc_de.save()

mcs_cs = mc.translations.filter(language = 'cs')
if mcs_cs.count() > 0:
    mc_cs = mcs_cs.first()
else:
    mc_cs = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'cs',
    )
mc_cs.display_name = 'Třída materiálu 2'
mc_cs.mat_class_description = 'něco v tunách'
mc_cs.save()

#----------------------------------------------------------------

mcs = AhMatClass.objects.filter(class_name = 'Material class 3')
if mcs.count() > 0:
    mc = mcs.first()
else:
    mc = AhMatClass(
        class_name = 'Material class 3',
        measurement_unit = 'ks.'
    )
    mc.save()

mcs_en = mc.translations.filter(language = 'en')
if mcs_en.count() > 0:
    mc_en = mcs_en.first()
else:
    mc_en = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'en',
    )
mc_en.display_name = 'Material class 3'
mc_en.mat_class_description = 'something in pieces'
mc_en.save()

mcs_de = mc.translations.filter(language = 'de')
if mcs_de.count() > 0:
    mc_de = mcs_de.first()
else:
    mc_de = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'de'
    )
mc_de.display_name = 'Materialklasse 3'
mc_de.mat_class_description = 'etwas in Stücke'
mc_de.save()

mcs_cs = mc.translations.filter(language = 'cs')
if mcs_cs.count() > 0:
    mc_cs = mcs_cs.first()
else:
    mc_cs = mc.translations.create(
        display_name = '',
        mat_class_description = '',
        language = 'cs',
    )
mc_cs.display_name = 'Třída materiálu 3'
mc_cs.mat_class_description = 'něco v kusech'
mc_cs.save()

#----------------------------------------------------------------
