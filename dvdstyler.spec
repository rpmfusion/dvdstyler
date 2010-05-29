Name:           dvdstyler
Epoch:          1
Version:        1.8.0.3
Release:        1%{?dist}
Summary:        Cross-platform DVD authoring application

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.dvdstyler.de/
Source0:        http://downloads.sourceforge.net/dvdstyler/DVDStyler-%{version}.tar.bz2
Patch0:         dvdstyler-make-desktopfile-valid.patch
Patch1:         dvdstyler-1.8-libjpeg.patch
Patch2:         dvdstyler-1.8-template-subdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# build
BuildRequires:  automake, autoconf, gettext
# libraries
BuildRequires:  wxGTK-devel >= 2.6.3
BuildRequires:  wxsvg-devel >= 1.0-6
BuildRequires:  ffmpeg-devel
BuildRequires:  libgnomeui-devel
# mpeg
BuildRequires:  dvdauthor
# iso/burn
BuildRequires:  mkisofs
BuildRequires:  dvd+rw-tools
#images
BuildRequires:  libjpeg-devel
BuildRequires:  libexif-devel
# documentation
BuildRequires:  zip
BuildRequires:  xmlto

BuildRequires:  desktop-file-utils

Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       mkisofs
Requires:       mpgtx
Requires:       wxsvg >= 1.0-6
# note: do not add Require: totem-backend or another DVD player - see
# RPM Fusion bug 366 for more details

%description
DVDStyler is a cross-platform DVD authoring application that makes possible for
video enthusiasts to create professional-looking DVDs. It allows users to
create navigational DVD menus similar to those found on most commercial DVDs.


%prep
%setup -q -n DVDStyler-%{version}
%patch0 -b .nonvalid
%patch1 -b .libjpeg
%patch2 -b .templates
%{__sed} -i 's|_T("xine \\"dvd:/$DIR\\"");|_T("totem \\"dvd://$DIR\\"");|' src/Config.h

%build
./autogen.sh
%configure \
  --disable-dependency-tracking
# docs folder is not smp_mflags safe
make -C docs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/dvdstyler

desktop-file-install --vendor rpmfusion \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/*/*.gz

%changelog
* Wed May 19 2010 Stewart Adam <s.adam at diffingo.com> - 1:1.8.0.3-1
- Update to 1.8.0.3
- Remove some of the outdated Requires and BuildRequires

* Sat Oct 24 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.4-1
- Update to 1.7.4

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.7.3-0.2.beta3
- rebuild for new ffmpeg

* Fri Jun 19 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.3-0.1.beta3
- Update to 1.7.3 beta3
- Remove gcc44 patch

* Tue Apr 7 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.2-3
- Add patch to fix gcc 4.4-related build errors

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.7.2-2
- rebuild for new F11 features

* Sun Mar 8 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.2-1
- Remove dependency on totem-backend (#366)
- Update to 1.7.2

* Sat Jan 24 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-4
- Remove wxsvg_freeworld patch
- desktop and icon files now install correctly, don't install them manually
- Remove hicolor scriptlets
- Update %%description

* Fri Jan 23 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-3
- Bump for proper upgrade path from F-10

* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-2
- Remove previous link hacks and link against wxsvg_freeworld
- Use totem to preview DVDs
- Don't require dvdisaster; it's optional
- Fix changelog dates wrt epoch

* Thu Nov 13 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-1
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
