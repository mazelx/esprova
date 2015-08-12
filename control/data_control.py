from events.models import Event, Race
from datetime import datetime
import re

def control_carryall_events():
    for e in Event.objects.filter(validated=True):
        p = e.get_potential_carryall()
        if p:
            print('EVENT : {0} ({1})'.format(e, e.pk))

            for r in e.races.all():
                print('{0}:{1} - {2} - {3}'.format(r.pk, r, r.date.strftime('%d/%m/%Y'), r.location))

            for s_dict in p:
                print('suspect: {0} ({1})'.format(s_dict['race'].pk, s_dict['distance']))

            created_race = 0
            for r in e.races.all():
                print('for {0}'.format(r.pk))

                while True:
                    ipt = input("'new'/<event pk>/'pass':")
                    if ipt in ('pass', 'p'):
                        print('passed')
                        break

                    elif ipt in ('new', 'n'):
                        cloned_event = e.clone()
                        cloned_event.name = cloned_event.name + '_auto_' + datetime.now().strftime('%Y%m%d_%H%M')
                        cloned_event.event_mod_source = None
                        cloned_event.save()
                        for cloned_race in cloned_event.races.all():
                            if cloned_race.race_mod_source.pk != r.pk:
                                cloned_race.delete()
                            else:
                                cloned_race.race_mod_source = None
                                cloned_race.save()

                        print('event created: {0}'.format(cloned_event.pk))
                        created_race += 1
                        break

                    elif ipt.isdigit():
                        try:
                            new_e = Event.objects.get(pk=int(ipt))
                            if new_e.validated:
                                new_e = new_e.clone()
                            new_r = r.clone()
                            new_r.event = new_e
                            new_r.save()
                            break
                        except Event.DoesNotExist:
                            print('event {0} not found...'.format(ipt))

            if (created_race == len(e.races.all())):
                if input('delete (soft) source event (y/N) ? ') in ('y', 'Y'):
                    cloned_event = e.clone()
                    cloned_event.to_be_deleted = True
                    cloned_event.save()
                    print('event {0} soft deleted (to be validated)'.format(e.pk))


def control_empty_events():
    for e in Event.objects.all():                  
        if len(e.races.all()) == 0:
            print('EVENT EMPTY : {0} - {1}'.format(e.pk, e))
            if input('delete event (y/N) ? ') in ('y', 'Y'):
                e.delete()

def control_empty_strings_event_name(interactive=True):
    for e in Event.objects.all():
        name = e.name
        new_name = name.strip()
        if not name == new_name:
            if interactive:
                if input('EVENT {0}: Replace "{1}" by "{2}" ? (y/N)'.format(e.pk, name, new_name)) not in ('y', 'Y'):
                    continue
            e = e.clone()
            e.name = new_name
            e.save()

def control_first_cap_event_name(interactive=True):
    for e in Event.objects.all():
        name = e.name
        lst = []
        for k,w in enumerate(name.split()):
            if k == 0:
                w = w.capitalize()
            lst.append(w)
        new_name = ' '.join(lst)

        if not name == new_name:
            if interactive:
                ipt = input('EVENT {0}: Replace "{1}" by "{2}" ? [y / N /o (other)]'.format(e.pk, name, new_name))
                if ipt not in ('y', 'Y', 'o'):
                    continue
                elif ipt in ('o'):
                    new_name = input('New name : ')
            e = e.clone()
            e.name = new_name
            e.save()


def control_edition_number_event_name(interactive=True):
    for e in Event.objects.all():
        name = e.name
        re_edition = re.compile('(\d+)')
        re_edition_prefix = re.compile('\d+\s?(?:°|ième|ieme|eme|ème|er|e|E)?')
        match = re_edition.match(name)
        if match:
            edition_no = match.group(0)
            print("EVENT {0}: {1} ".format(e.pk, e.name))
            edition_ipt = input('edition no : {0} ? [y/N/<editon no>]'.format(edition_no))

            if edition_ipt not in ('y', 'Y') and not edition_ipt.isdigit():
                continue

            elif edition_ipt.isdigit():
                edition_no = int(edition_ipt)

            new_name = name.replace(re_edition_prefix.match(name).group(0), '').strip()
            print('found {0}'.format(re_edition_prefix.match(name).group(0)))
            name_ipt = input('replace "{0}" by "{1}" ? [y/N/o]'.format(name, new_name))

            if name_ipt not in ('y', 'Y', 'o', 'O'):
                continue

            elif name_ipt in ('o', 'O'):
                new_name = input('New name : ')

                if e.validated:
                    new_e = e.clone()
                else:
                    new_e = e

            new_e.name = new_name
            new_e.edition = edition_no
            new_e.save()
            print('saved')


def control_year_event_name():
    for e in Event.objects.all():
        year = datetime.now().strftime('%Y')
        if year in e.name:
            print("EVENT {0}: {1} ".format(e.pk, e.name))
            name = e.name
            new_name = e.name.replace(year, '').strip()
            name_ipt = input('replace "{0}" by "{1}" ? [y/N/o]'.format(name, new_name))

            if name_ipt not in ('y', 'Y', 'o', 'O'):
                continue

            elif name_ipt in ('o', 'O'):
                new_name = input('New name : ')

                if e.validated:
                    new_e = e.clone()
                else:
                    new_e = e

            new_e.name = new_name
            new_e.save()
            print('saved')


def control_empty_event():
    for e in Event.objects.all():
        if e.races.all().count() == 0:
            print("EVENT {0}: {1} ".format(e.pk, e.name))
            if input('delete event ? [y/N] ') in ('y', 'Y'):
                if e.validated:
                    new_e = e.clone()
                else:
                    new_e = e

                new_e.to_be_deleted = True
                new_e.save()
                print('saved')


def control_administrative_area_missing():
    for e in Event.objects.all():
        for r in e.races.all():
            retry = False
            l = r.location

            if not l.administrative_area_level_1:
                print('missing area level 1')
                retry = True
            if not l.administrative_area_level_2_short_name:
                print('missing area level 2')
                retry = True

            if retry:
                print('{0} : initial address = {1}'.format(r.pk, l))
                ctry = input('country: ')
                address = input('new lookup address: ')
                res = l.geocode_raw_address(country=ctry, raw_address=address)
                print(res)
                if input('save ? [Y/n] ') not in ('n', 'N'):
                    l.save()
                    print('saved')
