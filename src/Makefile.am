MAINTAINERCLEANFILES = Makefile.in
MODULE = wizard

pkgdir                 = $(libdir)/enlightenment/modules/$(MODULE)/$(MODULE_ARCH)
pkg_LTLIBRARIES        = page_300.la

page_300_la_SOURCES      = page_300.c
page_300_la_LIBADD       = @e_libs@ @dlopen_libs@
page_300_la_LDFLAGS      = -module -avoid-version
page_300_la_DEPENDENCIES = $(top_builddir)/config.h

uninstall:
	rm -rf $(DESTDIR)$(libdir)/enlightenment/modules/$(MODULE)/page_300.*