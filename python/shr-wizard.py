#!/usr/bin/env python
import elementary
import dbus, e_dbus
from gettext import Catalog

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
    next.label_set(_('Finish'))
  else:
    next.label_set(_('Next'))

  if page==0:
    prev.disabled_set(True)
  else:
    prev.disabled_set(False)
  prev.label_set(_('Previous'))

def prev_page(*args, **kargs):
  global page
  page = page - 1
  pager.content_pop()
  update_bottom()

def next_page(*args, **kargs):
  global page
  if pageMods[page].wizardClose():
    page = page + 1
    render_page(page)

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
      header.scale_set(1.5)
      header.label_set(pageMod.wizard_name)
      header.show()
      bbox.pack_start(header)
      scr = elementary.Scroller(bbox)
      scr.size_hint_align_set(-1.0, -1.0)
      scr.size_hint_weight_set(1.0, 1.0)
      bbox.pack_end(scr)
      box = elementary.Box(scr)
      box.size_hint_align_set(-1.0, -1.0)
      box.size_hint_weight_set(1.0, 1.0)
      anc = elementary.AnchorBlock(pager)
      anc.text_set(pageMod.wizard_description)
      anc.show()
      ancfr = elementary.Frame(pager)
      ancfr.style_set('outdent_top')
      ancfr.content_set(anc)
      ancfr.size_hint_align_set(-1.0, 1.0)
      ancfr.size_hint_weight_set(1.0, 1.0)
      ancfr.show()
      box.pack_start(ancfr)
      cont.size_hint_align_set(-1.0, -1.0)
      cont.size_hint_weight_set(1.0, 1.0)
      box.pack_end(cont)
      box.show()
      scr.content_set(box)
      scr.bounce_set(False, False)
      scr.show()
      pager.content_push(bbox)
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
win.destroy = destroy
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

pager = elementary.Pager(inwin)
pager.size_hint_align_set(-1.0, -1.0)
pager.size_hint_weight_set(1.0, 1.0)
pager.show()
box.pack_end(pager)

bottom = elementary.Box(inwin)
bottom.horizontal_set(True)
bottom.homogenous_set(True)
bottom.size_hint_align_set(-1.0, 0.0)
bottom.size_hint_weight_set(1.0, 0.0)
bottom.show()
box.pack_end(bottom)

prev = elementary.Button(inwin)
prev.disabled_set(True)
prev.size_hint_align_set(-1.0, 0.0)
prev.size_hint_weight_set(1.0, 0.0)
prev.label_set(_('Previous'))
prev.show()
prev.clicked = prev_page
bottom.pack_start(prev)

next = elementary.Button(inwin)
next.label_set(_('Next'))
next.size_hint_align_set(-1.0, 0.0)
next.size_hint_weight_set(1.0, 0.0)
next.show()
next.clicked = next_page
bottom.pack_end(next)

page = 0
pageMods = []
pages = ['shr_phoneutils.Phoneutils', 'shr_gprs.Gprs']
render_page(page)

elementary.run()
elementary.shutdown()

