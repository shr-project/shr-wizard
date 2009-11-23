MAINTAINERCLEANFILES = Makefile.in
MODULE = wizard
#manual hack until I found out how to take e's release version
release=ver-pre-svn-04
MODULE_ARCH="$(host_os)-$(host_cpu)-$(release)"

AM_CFLAGS = -Wall @ENLIGHTENMENT_CFLAGS@

pkgdir                 = $(libdir)/enlightenment/modules/$(MODULE)/$(MODULE_ARCH)
pkg_LTLIBRARIES        = page_900.la

page_900_la_SOURCES      = page_900.c locations.h e_mod_main.h  e_wizard.h 
page_900_la_LIBADD       = @ENLIGHTENMENT_LIBS@ 
page_900_la_LDFLAGS      = -module -avoid-version

uninstall:
	rm -rf $(DESTDIR)$(libdir)/enlightenment/modules/$(MODULE)/page_900.*
