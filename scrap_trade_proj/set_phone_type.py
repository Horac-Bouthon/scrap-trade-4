from customers.models import (
    BasicPhoneCategory,
    BasicPhoneCategoryTranslation,
)

phones = BasicPhoneCategory.objects.filter(phone_type = 'phone')
if phones.count() > 0:
    phone = phones.first()
else:
    phone = BasicPhoneCategory(
        phone_type = 'phone',
    )
    phone.save()

phones_en = phone.translations.filter(language = 'en')
if phones_en.count() > 0:
    phone_en = phones_en.first()
else:
    phone_en = phone.translations.create(
        category = '',
        language = 'en',
    )
phone_en.category = 'phone'
phone_en.save()

phones_de = phone.translations.filter(language = 'de')
if phones_de.count() > 0:
    phone_de = phones_de.first()
else:
    phone_de = phone.translations.create(
        category = '',
        language = 'de'
    )
phone_de.category = 'Festnetz'
phone_de.save()

phones_cs = phone.translations.filter(language = 'cs')
if phones_cs.count() > 0:
    phone_cs = phones_cs.first()
else:
    phone_cs = phone.translations.create(
        category = '',
        language = 'cs',
    )
phone_cs.category = 'Pevná linka'
phone_cs.save()


#------------------------


mobiles = BasicPhoneCategory.objects.filter(phone_type = 'mobile')
if mobiles.count() > 0:
    mobile = mobiles.first()
else:
    mobile = BasicPhoneCategory(
        phone_type = 'mobile',
    )
    mobile.save()

mobiles_en = mobile.translations.filter(language = 'en')
if mobiles_en.count() > 0:
    mobile_en = mobiles_en.first()
else:
    mobile_en = mobile.translations.create(
        category = '',
        language = 'en',
    )
mobile_en.category = 'mobile'
mobile_en.save()

mobiles_de = mobile.translations.filter(language = 'de')
if mobiles_de.count() > 0:
    mobile_de = mobiles_de.first()
else:
    mobile_de = mobile.translations.create(
        category = '',
        language = 'de',
    )
mobile_de.category = 'Mobile'
mobile_de.save()

mobiles_cs = mobile.translations.filter(language = 'cs')
if mobiles_cs.count() > 0:
    mobile_cs = mobiles_cs.first()
else:
    mobile_cs = mobile.translations.create(
        category = '',
        language = 'cs'
    )
mobile_cs.category = 'mobil'
mobile_cs.save()

#------------------------


faxs = BasicPhoneCategory.objects.filter(phone_type = 'fax')
if faxs.count() > 0:
    fax = faxs.first()
else:
    fax = BasicPhoneCategory(
        phone_type = 'fax',
    )
    fax.save()

faxs_en = fax.translations.filter(language = 'en')
if faxs_en.count() > 0:
    fax_en = faxs_en.first()
else:
    fax_en = fax.translations.create(
        category = '',
        language = 'en',
    )
fax_en.category = 'fax'
fax_en.save()

faxs_de = fax.translations.filter(language = 'de')
if faxs_de.count() > 0:
    fax_de = faxs_de.first()
else:
    fax_de = fax.translations.create(
        category = '',
        language = 'de',
    )
fax_de.category = 'Faxgerät'
fax_de.save()

faxs_cs = fax.translations.filter(language = 'cs')
if faxs_cs.count() > 0:
    fax_cs = faxs_cs.first()
else:
    fax_cs = fax.translations.create(
        category = '',
        language = 'cs',
    )
fax_cs.category = 'fax'
fax_cs.save()
