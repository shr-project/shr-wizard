#!/usr/bin/env python
import os
import elementary
import dbus, e_dbus
from gettext import Catalog

pages = ['shr_phoneutils.Phoneutils', 'shr_gprs.Gprs', 'shr_passwd.Password', 'shr_firmware.Firmware']

try:
  cat = Catalog("shr-wizard")
  _ = cat.gettext
except IOError:
  _ = lambda x: x

print "SHR Wizard"

def destroy(*args,**kwargs):
  print 'kabum!'
  elementary.exit()

def update_bottom():
  if page==len(pages)-1:
    next.text_set(_('Finish'))
  else:
    next.text_set(_('Next'))

  if page==-1:
    prev.text_set(_('Exit wizard'))
  else:
    prev.text_set(_('Previous'))

def prev_page(*args, **kargs):
  global page
  page = page - 1
  if page==-2:
    destroy()
  pager.item_pop()
  update_bottom()

def next_page(*args, **kargs):
  global page
  try:
    if page==-1 or pageMods[page].wizardClose():
      page = page + 1
      render_page(page)
  except:
    # TODO: show error
    page = page + 1
    render_page(page)
  update_bottom()

def render_page(i):
  global pageMods
  if len(pages)<=i:
    destroy()
    return True
  else:
    (submodname, classname) = pages[i].split('.',1)
    module   = __import__('shr_settings_modules.' + submodname,
                                globals(), locals(), classname)
    ModClass = module.__getattribute__(classname)
    pageMod = ModClass(win, bus, True)
    try:
      pageMods[i] = pageMod
    except:
      pageMods.append(pageMod)
    if pageMod.isEnabled():
      cont = pageMod.createView()
      bbox = elementary.Box(pager)
      bbox.show()
      header = elementary.Label(bbox)
      header.scale_set(1.4)
      header.text_set(pageMod.wizard_name)
      header.show()

      anc = elementary.Entry(pager)
      anc.size_hint_align_set(-1.0, 1.0)
      anc.size_hint_weight_set(0.0, 0.0)
      anc.text_set(pageMod.wizard_description)
      anc.scale_set(0.90)
      anc.show()

      bbox.pack_start(header)
      bbox.pack_end(anc)
      scr = elementary.Scroller(bbox)
      scr.size_hint_align_set(-1.0, -1.0)
      scr.size_hint_weight_set(1.0, 1.0)
      bbox.pack_end(scr)

      cont.size_hint_align_set(-1.0, -1.0)
      cont.size_hint_weight_set(1.0, 1.0)
      scr.policy_set(0, 1)
      scr.content_set(cont)
      scr.bounce_set(False, False)
      scr.show()
      pager.item_simple_push(bbox)
    else:
      next_page()

  update_bottom()

elementary.init()

mainloop = e_dbus.DBusEcoreMainLoop()
bus = dbus.SystemBus(mainloop=mainloop)

win = elementary.Window('shrwizard',0);
bg = elementary.Background(win)
bg.show()
win.title_set('Wizard')
win.callback_delete_request_add(destroy)
win.show()
win.resize_object_add(bg)
win.fullscreen_set(True)

inwin = elementary.InnerWindow(win)
win.resize_object_add(inwin)
inwin.show()
inwin.activate()

box = elementary.Box(win)
box.show()
inwin.content_set(box)

pager = elementary.Naviframe(inwin)
pager.size_hint_align_set(-1.0, -1.0)
pager.size_hint_weight_set(1.0, 1.0)
pager.show()
box.pack_end(pager)

bottom = elementary.Box(inwin)
bottom.horizontal_set(True)
bottom.homogeneous_set(True)
bottom.size_hint_align_set(-1.0, 0.0)
bottom.size_hint_weight_set(1.0, 0.0)
bottom.show()
box.pack_end(bottom)

prev = elementary.Button(inwin)
prev.size_hint_align_set(-1.0, 0.0)
prev.size_hint_weight_set(1.0, 0.0)
prev.text_set(_('Exit Wizard'))
prev.show()
prev._callback_add('clicked', prev_page)
bottom.pack_start(prev)

next = elementary.Button(inwin)
next.text_set(_('Next'))
next.size_hint_align_set(-1.0, 0.0)
next.size_hint_weight_set(1.0, 0.0)
next.show()
next._callback_add('clicked', next_page)
bottom.pack_end(next)

page = -1
pageMods = []

wel = elementary.Entry(pager)
wel.text_set(_('<b>Welcome to SHR Wizard!</b><br><br>This is a first-run configuration wizard, used to get the most important informations needed by SHR.<br><br><b>NOTE:</b> You can also adjust all of those settings later in SHR Settings.'))
wel.show()
pager.item_simple_push(wel)

#small hacks needed to run after ~/.e creation
os.system( "mkdir -p ~/.e/e/applications/startup/" )
os.system( "echo shr_elm_softkey.desktop > ~/.e/e/applications/startup/.order" )
os.system( "pgrep shr_elm_softkey || shr_elm_softkey >/dev/null </dev/null &" )
#os.system( "mv ~/.e/e/appshadow/* /var/volatile/appshadow/" )
#os.system( "rm -rf ~/.e/e/appshadow/" )
#os.system( "ln -s /var/volatile/appshadow/ ~/.e/e/appshadow" )

elementary.run()
elementary.shutdown()
