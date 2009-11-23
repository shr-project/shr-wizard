MAINTAINERCLEANFILES = Makefile.in
MODULE = wizard
MODULE_ARCH="$host_os-$host_cpu-$release"

AM_CFLAGS = -Wall @ENLIGHTENMENT_CFLAGS@

pkgdir                 = $(libdir)/enlightenment/modules/$(MODULE)/$(MODULE_ARCH)
pkg_LTLIBRARIES        = page_900.la

page_900_la_SOURCES      = page_900.c
page_900_la_LIBADD       = @ENLIGHTENMENT_LIBS@ @dlopen_libs@
page_900_la_LDFLAGS      = -module -avoid-version

uninstall:
	rm -rf $(DESTDIR)$(libdir)/enlightenment/modules/$(MODULE)/page_900.*
