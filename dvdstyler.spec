Name:           dvdstyler
Epoch:          1
Version:        1.7.1
Release:        2%{?dist}
Summary:        Cross-platform DVD authoring application

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.dvdstyler.de/
Source0:        http://downloads.sourceforge.net/dvdstyler/DVDStyler-%{version}.tar.bz2
Patch0:         dvdstyler-1.6.2-desktop.patch
Patch1:         dvdstyler-1.7.1-wxsvg_freeworld.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# build
BuildRequires:  automake, autoconf, gettext
# libraries
BuildRequires:  wxGTK-devel >= 2.6.3
BuildRequires:  wxsvg-devel >= 1.0
BuildRequires:  ffmpeg-devel
BuildRequires:  libgnomeui-devel
# mpeg
BuildRequires:  mpgtx
BuildRequires:  mjpegtools
BuildRequires:  dvdauthor
# iso/burn
BuildRequires:  mkisofs
BuildRequires:  dvd+rw-tools
#images
BuildRequires:  libjpeg-devel
BuildRequires:  libexif-devel
BuildRequires:  netpbm-progs
# finally
BuildRequires:  desktop-file-utils

Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       mkisofs
Requires:       mpgtx
Requires:       netpbm-progs
Requires:       wxsvg-freeworld >= 1.0
# Don't care what backend, but we need one to preview DVDs.
Requires:       totem-backend
# Optional, defaults to off in burn settings in 1.5.1
#Requires(hint): dvdisaster

%description
DVDStyler is a cross-platform DVD menu creation GUI that allows
creation of DVD navigation menus similar to those found on most
commercial DVD's.  It leverages various other open source video
rendering programs to produce the final DVD menu navigation system.


%prep
%setup -q -n DVDStyler-%{version}
%patch0 -b .desktop
%patch1 -b .wxsvg_freeworld
%{__sed} -i 's|_T("xine \\"dvd:/$DIR\\"");|_T("totem \\"dvd://$DIR\\"");|' src/Config.h

%build
./autogen.sh
%configure \
  --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/dvdstyler
# Desktop entry and icon are supposed to be installed by "make install"
# in 1.5.1 (to paths we don't want) but are not due to configure/Makefile.in
# and friends outdatedness, watch this space in > 1.5.1.
desktop-file-install --vendor livna --mode 644 \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  data/dvdstyler.desktop
install -Dpm 644 data/dvdstyler.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/dvdstyler.png

%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/dvdstyler
%{_datadir}/dvdstyler/
%{_datadir}/applications/*dvdstyler.desktop
%{_datadir}/icons/hicolor/*x*/apps/dvdstyler.png
%{_datadir}/pixmaps/dvdstyler.png
%{_mandir}/*/*.gz

%changelog
* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-2
- Remove previous link hacks and link against wxsvg_freeworld
- Use totem to preview DVDs
- Don't require dvdisaster; it's optional
- Fix changelog dates wrt epoch

* Thu Nov 13 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-2
- Update to 1.7.1
- Remove AVCodecTag patch
- Add wxsvg-freeworld to the linker paths

* Wed Oct 15 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-3
- Add ffmpeg-devel and fix wxsvg-freeworld-devel BR
- Add patch to fix AVCodecTag conversion errors
- Update wxsvg-freeworld patch so dvdstyler can be built without wxsvg (and use
  only wxsvg-freeworld instead)

* Sat Sep 27 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-2
- Rebuild for wxsvg 1.0b11 with ffmpeg enabled

* Sat Sep 06 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-1
- Update to 1.7.0

* Sat Aug 16 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.6.2-1
- Update to 1.6.2

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:1.5.1-3
- rebuild

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.1-2
- License: GPL+
- Sync icon cache scriptlets with Fedora Wiki.

* Mon Jul  9 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.1-1
- 1.5.1.

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5-1
- 1.5.

* Fri May 25 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-8
- Rebuild.

* Tue Feb  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-7
- Patch for wxWidgets 2.8.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.4-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-5
- Rebuild.

* Sun Apr  9 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-4
- Actually apply the y4mscaler patch (#904).  Note that for the change to take
  effect, old Jpeg2MpegCmd setting may need to be removed from ~/.dvdstyler.
- Install icon to %%{_datadir}/icons/hicolor.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jun 06 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 1:1.4-0.lvn.3
- Add gcc4-x86_64.patch to fix compile on x86_64

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.lvn.2
- Patch default config to use y4mscaler and require it due to changes in
  mjpegtools 1.7.0.

* Wed May 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.lvn.1
- 1.4, desktop entry patch applied upstream.
- Patch to fix about dialog crash.

* Sun Jan 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.31-0.lvn.1
- First build.
