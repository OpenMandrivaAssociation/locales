#
# this spec file builds all the locales into rpm packages.
# it is separate from the glibc spec, so that it is possible to rebuild
# the locales for small fix without the need to rebuild the highly critical
# glibc package.
# however, locales adn glibc are very tied, so each time a new glibc is
# built, the locales have to be rebuilt too (on a system with the new glibc
# installed); and the glibc_ver define changed accordingly.
#
# the locales are mainly from the glibc-i18ndata; however, we include
# also fixes and improvements as well as some new locales; they should
# be included upstream ideally, so when new glibc is released, it is
# necessary to check if the separate locale files here are still needed.
# removing them is enough.
#
# we also use an improved iso14651_hack (used for the base collating
# definition) which improves the one in glibc (by defining collation for
# various extra letters in latin, greek, cyrillic and arabic scripts)
# and two scripts used by individual locales-*.rpm packages that add/remove
# the language names from the list of supported languages when adding/removing
# the package.
# All the rest of the sources are new or fixed locale files
#
%define glibc_ver 2.16.90
%define glibc_epoch 6
%define version   %{glibc_ver}
# FIXME: please check on next build those we really need
%define _unpackaged_files_terminate_build 1

# to define when building for PRC
%define build_for_PRC 0

# shorthands for the post scripts
%define loc_add /usr/bin/locale_install.sh
%define loc_del /usr/bin/locale_uninstall.sh

Summary:	Base files for localization
Name:		locales
Version:	%{glibc_ver}
Release:	1
License:	LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group:		System/Internationalization
Source0:	Makefile
# updated to include unicode 5.0 introduced latin/cyrullic/greek letters
#
Source1:	iso14651_hack
# scripts/config files to install/uninstall a locale
Source2:	locale_install.sh
Source3:	locale_uninstall.sh
Source4:	locales.sysconfig
Source5:	locales-hardlink.pl
Source6:	locales-softlink.pl

# this one is on glibc, however there is the politic issue
# of the naming of Taiwan 
Source15:	zh_TW_2
# locales data
Source16:	sw_XX
Source17:	ku_TR
Source18:	eo_XX
Source19:	ky_KG
Source22:	km_KH
Source25:	nds_DE@traditional
Source38:	dz_BT

# Those exist in glibc >= 2.3.2 but the attached ones
# are more correct/more complete

# all ar_?? locales in glibc 2.3.5 are missing "Yy" and "Nn" in 
# version in glibc 2.3.5 has wrong yexexpr/noexpr and wrong LC_COLLATE
Source50:	ar_SA
# corrected month names
Source51:	az_AZ
# LC_COLLATE has one line wrong
Source52:	bs_BA
# rewritten to take profit of new glibc reordering possibilities
Source53:	es_ES
Source54:	es_US
Source55:	es@tradicional
# Colombia uses "Letter" paper size
Source56:	es_CO
# corrected LC_COLLATE
Source58:	sq_AL
# ours has yesexpr using tajik
Source59:	tg_TJ
# tr_TR thet includes "i18n_tr" (generated with a simple regexp replacing)
Source61:	tr_TR
# LC_COLLATE for vietnamese is incorrect in glibc, and LC_CTIME seems
# wrong too... 
Source63:	vi_VN
# fixes in weekday names
Source64:	wa_BE
# various spelling fixes
Source65:	yi_US
# changed date format strings
Source66:	zh_CN

# ethiopic locales (violate ISO-639! not packaged)
Source67:	ad_ET
Source68:	qo_ET
Source69:	sx_ET
Source70:	sz_ET

# it is arch dependent in fact
#BuildArchitectures: noarch
# to build this package glibc = %{glibc_ver} is needed (for locales definitions)
# no need to check for dependencies when building, there is no executables here
AutoReqProv:	no
# locales are very dependent on glibc version
Requires:	glibc = %{glibc_epoch}:%{glibc_ver}
# post scripts use grep, perl, etc.
Requires(post):	perl-base rpm coreutils
Requires(postun):perl-base rpm coreutils
# glibc >= 2.2.5-6mdk now comes with glibc-i18ndata package
BuildRequires:	glibc-i18ndata >= %{glibc_epoch}:%{glibc_ver}
# usually needed to ensure support for new locales
BuildRequires:	glibc >= %{glibc_epoch}:%{glibc_ver}

%description
These are the base files for language localization.
You also need to install the specific locales-?? for the
language(s) you want. Then the user need to set the
LANG variable to their preferred language in their
~/.profile configuration file.

%post
%{loc_add} "ENCODINGS"

%preun
if [ "$1" = "0" ]; then
	%{loc_del} "ENCODINGS"
fi

%files
%config(noreplace) /etc/sysconfig/locales
%dir %{_localedir}
%{_localedir}/ISO*
%{_localedir}/CP*
%{_localedir}/UTF*
%{_localedir}/KOI*
/usr/bin/*



####################################################################
# The various localization packages.
#
# add one for each new language that is included in the future
####################################################################

### aa
%package -n locales-aa
Summary: Base files for localization (Afar)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-aa
These are the base files for Afar language localization; you need
it to correctly display 8bits Afar characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afar language conventions.

%post -n locales-aa
%{loc_add} aa_DJ aa_ER aa_ET

%preun -n locales-aa
if [ "$1" = "0" ]; then
	%{loc_del} aa_DJ aa_ER aa_ET
fi

%files -n locales-aa
%{_localedir}/aa_DJ*
%{_localedir}/aa_ER*
%{_localedir}/aa_ET*

### af
# translation by Schalk Cronje <schalkc@ntaba.co.za>
%package -n locales-af
Summary: Base files for localization (Afrikaans)
#Summary(af): Hierdie is die basislêers vir Afrikaanse lokalisasie
Group: System/Internationalization
URL: http://www.af.org.za/aflaai/linux-i18n/
Requires: locales = %{version}-%{release}

%description -n locales-af
These are the base files for Afrikaans language localization; you need
it to correctly display 8bits Afrikaans characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afrikaans language conventions.

#%#description -n locales-af -l af
#Hierdie is die basislêers vir Afrikaanse lokalisasie. U benodig dit om die
#Afrikaanse 8-bis karakters korrek te vertoon, vir korrekte alfabetiese
#sorterting en ook om datums en getalle in die Afrikaanse standaardvorm te
#vertoon.

%post -n locales-af
%{loc_add} af_ZA

%preun -n locales-af
if [ "$1" = "0" ]; then
	%{loc_del} af_ZA
fi

%files -n locales-af
%{_localedir}/af_ZA*

### am
# translation by Daniel Yacob <Yacob@EthiopiaOnline.Net>
%package -n locales-am
Summary: Base files for localization (Amharic)
#Summary(am): ለlocalization (አማርኛ) መሰረት ፋይሎች
Group: System/Internationalization
URL: http://www.ethiopic.org/
Requires: locales = %{version}-%{release}
Provides: locales-byn = %{version}-%{release}
Provides: locales-gez = %{version}-%{release}
Provides: locales-sid = %{version}-%{release}
Provides: locales-ti = %{version}-%{release}
Provides: locales-tig = %{version}-%{release}
Provides: locales-om = %{version}-%{release}
Provides: locales-wal = %{version}-%{release}

%description -n locales-am
These are the base files for Amharic language localization; you need
it to correctly display 8bits Amharic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amharic language conventions.

#%#description -n locales-am -l am
#እነዚህ ያማርኛ ቋንቋ localization  መሰረት ፋይሎች ናቸው።
#ያማርኛ ፊደላትንለማየት፣ የፊደላት ቅደም ተከተልን ለመጠበቅ፣
#ቀኖችንና ቍጥሮችንበቋንቋው ስርዓት ለማስቀመጥ ያስፈልጋሉ።

%post -n locales-am
%{loc_add} am_ET byn_ER gez_ER gez_ET om_ET om_KE sid_ET ti_ER ti_ET tig_ER \
           wal_ET

%preun -n locales-am
if [ "$1" = "0" ]; then
	%{loc_del} am_ET byn_ER gez_ER gez_ET om_ET om_KE sid_ET ti_ER ti_ET \
	           tig_ER wal_ET
fi

%files -n locales-am
%{_localedir}/am_ET*
# blin
%{_localedir}/byn_ER*
# tigrinya
%{_localedir}/ti_ER*
%{_localedir}/ti_ET*
# ge'ez
%{_localedir}/gez_ER*
%{_localedir}/gez_ET*
# sidama
%{_localedir}/sid_ET*
# tigre
%{_localedir}/tig_ER*
# Oromo
%{_localedir}/om_ET*
%{_localedir}/om_KE*
# Walaita
%{_localedir}/wal_ET*

### ar
# translation by Wajdi Al-Jedaibi <wajdi@acm.org>
%package -n locales-ar
Summary: Base files for localization (Arabic)
Summary(ar): هذه هي الملفات اللازمة لإعتماد اللغة العربية في نظام لينكس.
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ar
These are the base files for Arabic language localization; you need
it to correctly display 8bits arabic characters, and for proper
alfabetical sorting and representation of dates and numbers according
to arabic language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%description -n locales-ar -l ar
هذه هي الملفات اللازمة لإعتماد اللغة العربية في نظام لينكس.
لاحظ أن هذا البرنامجلايقوم بعملية تحويل اتجاه الكتابة من اليمن إلى
اليسار والعكس، ولكن يوفر الاساسيات الضرورية لعرض وتصنيف وترتيب الاحرف
العربية، بما في ذلك إظهار التاريخ و غيره.

%post -n locales-ar
%{loc_add} ar_AE ar_BH ar_DZ ar_EG ar_IN ar_IQ ar_JO ar_KW ar_LB ar_LY ar_MA \
           ar_OM ar_QA ar_SA ar_SD ar_SY ar_TN ar_YE

%preun -n locales-ar
if [ "$1" = "0" ]; then
	%{loc_del} ar_AE ar_BH ar_DZ ar_EG ar_IN ar_IQ ar_JO ar_KW ar_LB ar_LY \
	           ar_MA ar_OM ar_QA ar_SA ar_SD ar_SY ar_TN ar_YE
fi

%files -n locales-ar
%{_localedir}/ar_AE*
%{_localedir}/ar_BH*
%{_localedir}/ar_DZ*
%{_localedir}/ar_EG*
%{_localedir}/ar_IN*
%{_localedir}/ar_IQ*
%{_localedir}/ar_JO*
%{_localedir}/ar_KW*
%{_localedir}/ar_LB*
%{_localedir}/ar_LY*
%{_localedir}/ar_MA*
%{_localedir}/ar_OM*
%{_localedir}/ar_QA*
%{_localedir}/ar_SA*
%{_localedir}/ar_SD*
%{_localedir}/ar_SY*
%{_localedir}/ar_TN*
%{_localedir}/ar_YE*

### as
%package -n locales-as
Summary: Base files for localization (Assamese)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-as
These are the base files for Assamese language localization; you need
it to correctly display 8bits Assamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Assamese language conventions.

%post -n locales-as
%{loc_add} as_IN

%preun -n locales-as
if [ "$1" = "0" ]; then
	%{loc_del} as_IN
fi

%files -n locales-as
%{_localedir}/as_IN*

### ast
%package -n locales-ast
Summary: Base files for localization (Asturian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ast
These are the base files for Asturian language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Asturian language conventions.

%post -n locales-ast
%{loc_add} ast_ES

%preun -n locales-ast
if [ "$1" = "0" ]; then
	%{loc_del} ast_ES
fi

%files -n locales-ast
%{_localedir}/ast_ES*

### az
%package -n locales-az
Summary: Base files for localization (Azeri)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-az
These are the base files for Azeri language localization; you need
it to correctly display 8bits Azeri characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Azeri language conventions.

%post -n locales-az
%{loc_add} az_AZ

%preun -n locales-az
if [ "$1" = "0" ]; then
	%{loc_del} az_AZ
fi

%files -n locales-az
%{_localedir}/az_AZ*

### be
%package -n locales-be
Summary: Base files for localization (Belarussian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-be
These are the base files for Belarussian language localization; you need
it to correctly display 8bits Belarussian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Belarussian language conventions.

%post -n locales-be
%{loc_add} be_BY

%preun -n locales-be
if [ "$1" = "0" ]; then
	%{loc_del} be_BY
fi

%files -n locales-be
%{_localedir}/be_BY*

### bem
%package	bem
Summary:	Base files for localization (Bemba)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	bem
These are the base files for Bemba language localization; you need
it to correctly display 8bits Bemba characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bemba language conventions.

%post		bem
%{loc_add} bem_ZM

%preun		bem
if [ "$1" = "0" ]; then
	%{loc_del} bem_ZM
fi

%files		bem
%{_localedir}/bem_ZM*

### ber
%package -n locales-ber
Summary: Base files for localization (Berber)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ber
These are the base files for Berber (Amazigh) language localization; you need
it to correctly display 8bits Amazigh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amazigh language conventions.

%post -n locales-ber
%{loc_add} ber_DZ ber_MA

%preun -n locales-ber
if [ "$1" = "0" ]; then
	%{loc_del} ber_DZ ber_MA
fi

%files -n locales-ber
%{_localedir}/ber_DZ*
%{_localedir}/ber_MA*

### bg
# translation: Mariana Kokosharova <kokosharova@dir.bg>
%package -n locales-bg
Summary: Base files for localization (Bulgarian)
Summary(bg): съдържат основните регионални характеристики на българския език
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-bg
These are the base files for Bulgarian language localization; you need
it to correctly display 8bits Bulgarian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bulgarian language conventions.

%description -n locales-bg -l bg
Тези файлове съдържат основните регионални характеристики на българския език;
теса необходими за правилното представяне на 8 - битовите букви на кирилицата
на екрана, за правилната азбучна подредба и за представяне на датата и числата
в съответствие на правилата на българския език.

%post -n locales-bg
%{loc_add} bg_BG

%preun -n locales-bg
if [ "$1" = "0" ]; then
	%{loc_del} bg_BG
fi

%files -n locales-bg
%{_localedir}/bg_BG*

### bn
%package -n locales-bn
Summary: Base files for localization (Bengali)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-bn
These are the base files for Bengali language localization; you need
it to correctly display 8bits Bengali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bengali language conventions.

%post -n locales-bn
%{loc_add} bn_BD bn_IN

%preun -n locales-bn
if [ "$1" = "0" ]; then
	%{loc_del} bn_BD bn_IN
fi

%files -n locales-bn
%{_localedir}/bn_BD*
%{_localedir}/bn_IN*

### bo
%package -n locales-bo
Summary: Base files for localization (Tibetan language)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-bo
These are the base files for Tibetan language localization; you need
it to correctly display 8bits Tibetan characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tibetan language conventions.

%post -n locales-bo
%{loc_add} bo_CN bo_IN

%preun -n locales-bo
if [ "$1" = "0" ]; then
	%{loc_del} bo_CN bo_IN
fi

%files -n locales-bo
%{_localedir}/bo_CN*
%{_localedir}/bo_IN*

### br
# Translation by Jañ-Mai Drapier (jan-mai-drapier@mail.dotcom.fr)
%package -n locales-br
Summary: Base files for localization (Breton)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue bretonne
Summary(br): Kement-mañ a zo restroù diazez evit broelañ diouzh ar brezhoneg

%description -n locales-br
These are the base files for Breton language localization; you need
it to correctly display 8bits Breton characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Breton language conventions.

%description -n locales-br -l fr
Ce paquet contient les définitions de locales en langue brétonne.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates et des nombres.

%description -n locales-br -l br
Kement-mañ a zo restroù diazez evit broelañ diouzh ar Vrezhoneg; ret eo
evit diskwel ent reizh arouezennoù breizhat 8bit, rummañ dre al
lizherenneg, taolennañ an deizadoù hag an niveroù hervez kendivizadoù ar
brezhoneg.

%post -n locales-br
%{loc_add} br_FR

%preun -n locales-br
if [ "$1" = "0" ]; then
	%{loc_del} br_FR
fi

%files -n locales-br
%{_localedir}/br_FR*

### bs
%package -n locales-bs
Summary: Base files for localization (Bosnian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-bs
These are the base files for Bosnian language localization; you need
it to correctly display 8bits Bosnian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bosnian language conventions.

%post -n locales-bs
%{loc_add} bs_BA

%preun -n locales-bs
if [ "$1" = "0" ]; then
	%{loc_del} bs_BA
fi

%files -n locales-bs
%{_localedir}/bs_BA*

### ca
%package -n locales-ca
Summary: Base files for localization (Catalan)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(ca): Arxius bàsics per a l'adaptació al català
Summary(es): Archivos de base para la localización en idioma catalán
Summary(fr): Fichiers de base pour la localisation en langue catalane

%description -n locales-ca
These are the base files for Catalan language localization; you need
it to correctly display 8bits Catalan characters, and for proper
representation of dates, numbers and alphabetical order according to
Catalan language conventions

%description -n locales-ca -l ca
Aquests són els arxius bàsics per a l'adaptació del sistema a les
peculiaritats de la llengua catalana; són necessaris perquè les
vocals accentuades, la ce trencada, etc. apareguin correctament, i
perquè les dates, els nombres i l'ordre alfabètic s'adaptin a les
convencions de la dita llengua.

%description -n locales-ca -l es
Este paquete incluye las definiciones de locales para el catalán.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del catalán, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del catalán.

%description -n locales-ca -l fr
Ce paquet contient les définitions de locales en langue catalane.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%post -n locales-ca
%{loc_add} ca_AD ca_ES ca_FR ca_IT

%preun -n locales-ca
if [ "$1" = "0" ]; then
	%{loc_del} ca_AD ca_ES ca_FR ca_IT
fi

%files -n locales-ca
%{_localedir}/ca_AD*
%{_localedir}/ca_ES*
%{_localedir}/ca_FR*
%{_localedir}/ca_IT*

### crh
%package -n locales-crh
Summary: Base files for localization (Crimean Tatar)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-crh
These are the base files for Crimean Tatar language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Crimean Tatar language conventions.

%post -n locales-crh
%{loc_add} crh_UA

%preun -n locales-crh
if [ "$1" = "0" ]; then
	%{loc_del} crh_UA
fi

%files -n locales-crh
%{_localedir}/crh_UA

### cs
# translation by <pavel@SnowWhite.inet.cz>
%package -n locales-cs
Summary: Base files for localization (Czech)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(cs): Základní soubory pro lokalizaci (čeština)

%description -n locales-cs
These are the base files for Czech language localization; you need
it to correctly display 8bits Czech characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Czech language conventions.

%description -n locales-cs -l cs
Zde jsou soubory nutné pro správnou českou lokalizaci; potřebujete je
pro správné zobrazování českých 8bitových znaků a pro správné české
třídění a reprezentaci data a čísel podle českých konvencí.

%post -n locales-cs
%{loc_add} cs_CZ

%preun -n locales-cs
if [ "$1" = "0" ]; then
	%{loc_del} cs_CZ
fi

%files -n locales-cs
%{_localedir}/cs_CZ*

### cv
%package -n locales-cv
Summary: Base files for localization (Chuvash)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-cv
These are the base files for Chuvash language localization; you need
it to correctly display 8bits Chuvash characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Chuvash language conventions.

%post -n locales-cv
%{loc_add} cv_RU

%preun -n locales-cv
if [ "$1" = "0" ]; then
	%{loc_del} cv_RU
fi

%files -n locales-cv
%{_localedir}/cv_RU*

### cy
%package -n locales-cy
Summary: Base files for localization (Welsh)
Summary(cy): Dyma'r ffeiliau sylfaenol i'r lleoliaeth Cymraeg
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-cy
These are the base files for Welsh language localization; you need
it to correctly display 8bits Welsh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Welsh language conventions.

%description -n locales-cy -l cy
Dyma'r ffeiliau sylfaenol i'r lleoliaeth Cymraeg; mae angen rhain er mwyn
dangos yn iawn y cymeriadau Cymraeg 8-bit, a threfniant y wyddor,
dyddiadau a rhifau yn ôl yr arfer Cymraeg.

%post -n locales-cy
%{loc_add} cy_GB

%preun -n locales-cy
if [ "$1" = "0" ]; then
	%{loc_del} cy_GB
fi

%files -n locales-cy
%{_localedir}/cy_GB*

### da
# danish translation by Erik Martino <martino@daimi.au.dk>
%package -n locales-da
Summary: Base files for localization (Danish)
Summary(da): Her er de basale filer for dansk sprog tilpasning
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-da
These are the base files for Danish language localization; you need
it to correctly display 8bits Danish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Danish language conventions.

%description -n locales-da -l da
Her er de basale filer for dansk sprog tilpasning. De er nødvendige for
at vise de danske 8bit tegn, sortere alfabetisk og repræsentere datoer
og tal korrekt ifølge dansk retskrivning.


%post -n locales-da
%{loc_add} da_DK

%preun -n locales-da
if [ "$1" = "0" ]; then
	%{loc_del} da_DK
fi

%files -n locales-da
%{_localedir}/da_DK*

### de
%package -n locales-de
Summary: Base files for localization (German)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue allemande
Summary(de): Basisdateien für die Lokalisierung (deutsch)

%description -n locales-de
These are the base files for German language localization; you need
it to correctly display 8bits German characters, and for proper
alphabetical sorting and representation of dates and numbers according
to German language conventions.

%description -n locales-de -l fr
Ce paquet contient les définitions de locales en langue allemande.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%description -n locales-de -l de
Dies sind die Basisdateien für die deutsche Sprachanpassung; sie
werden für die korrekte Darstellung deutscher 8-Bit-Zeichen,
die deutsche Sortierreihenfolge sowie Datums- und Zahlendarstellung
benötigt.

%post -n locales-de
%{loc_add} de_AT de_BE de_CH de_DE de_LU

%preun -n locales-de
if [ "$1" = "0" ]; then
	%{loc_del} de_AT de_BE de_CH de_DE de_LU
fi

%files -n locales-de
%{_localedir}/de_AT*
%{_localedir}/de_BE*
%{_localedir}/de_CH*
%{_localedir}/de_DE*
%{_localedir}/de_LU*

### doi
%package -n locales-doi
Summary: Base files for localization (Dogri)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-doi
These are the base files for Dogri language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Dogri language conventions.

%post -n locales-doi
%{loc_add} doi_IN

%preun -n locales-doi
if [ "$1" = "0" ]; then
	%{loc_del} doi_IN
fi

%files -n locales-doi
%{_localedir}/doi_IN

### dv
%package -n locales-dv
Summary: Base files for localization (Dhivehi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-dv
These are the base files for Dhivehi language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Dhivehi language conventions.

%post -n locales-dv
%{loc_add} dv_MV

%preun -n locales-dv
if [ "$1" = "0" ]; then
	%{loc_del} dv_MV
fi

%files -n locales-dv
%{_localedir}/dv_MV

### dz
%package -n locales-dz
Summary: Base files for localization (Dzongkha)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-dz
These are the base files for Dzongkha language localization; you need
it to correctly display 8bits Dzongkha characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Dzongkha language conventions.

%post -n locales-dz
%{loc_add} dz_BT

%preun -n locales-dz
if [ "$1" = "0" ]; then
	%{loc_del} dz_BT
fi

%files -n locales-dz
%{_localedir}/dz_BT*

### el
# translations from "Theodore J. Soldatos" <theodore@eexi.gr>
%package -n locales-el
Summary: Base files for localization (Greek)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: locales-gr
Provides: locales-gr = %{version}-%{release}
Summary(el): Βασικά αρχεία τοπικών ρυθμίσεων (Ελληνικά)

%description -n locales-el
These are the base files for Greek language localization; you need
it to correctly display 8bits Greek characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Greek language conventions.

%description -n locales-el -l el
Αυτά είναι τα βασικά αρχεία για υποστήριξη ελληνικής γλώσσας. Τα χρειάζεστε
για τη σωστή απεικόνιση 8bit ελληνικών χαρακτήρων, καθώς και για την σωστή
ταξινόμηση και απεικόνιση ημερομηνιών και αριθμών σύμφωνα με τις συμβάσεις
της ελληνικής γλώσσας.

%post -n locales-el
%{loc_add} el_CY el_GR

%preun -n locales-el
if [ "$1" = "0" ]; then
	%{loc_del} el_CY el_GR
fi

%files -n locales-el
%{_localedir}/el_CY*
%{_localedir}/el_GR*

### en
%package -n locales-en
Summary: Base files for localization (English)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-en_GB = %{version}-%{release}
Provides: locales-en_IE = %{version}-%{release}
Provides: locales-en_CA = %{version}-%{release}
Provides: locales-en_US = %{version}-%{release}

%description -n locales-en
These are the base files for English language localization.
Contains: en_CA en_DK en_GB en_IE en_US

%post -n locales-en
%{loc_add} en_AG en_AU en_BE en_BW en_CA en_DK en_GB en_HK en_IE en_IN en_NG \
           en_NZ en_PH en_SG en_US en_ZA en_ZM en_ZW

%preun -n locales-en
if [ "$1" = "0" ]; then
	%{loc_del} en_AG en_AU en_BE en_BW en_CA en_DK en_GB en_HK en_IE en_IN \
	           en_NG en_NZ en_PH en_SG en_US en_ZA en_ZW
fi

%files -n locales-en
%{_localedir}/en_AG*
%{_localedir}/en_AU*
%{_localedir}/en_BE*
%{_localedir}/en_BW*
%{_localedir}/en_CA*
%{_localedir}/en_DK*
%{_localedir}/en_GB*
%{_localedir}/en_HK*
%{_localedir}/en_IE*
%{_localedir}/en_IN*
%{_localedir}/en_NG*
%{_localedir}/en_NZ*
%{_localedir}/en_PH*
%{_localedir}/en_SG*
%{_localedir}/en_US*
%{_localedir}/en_ZA*
%{_localedir}/en_ZM*
%{_localedir}/en_ZW*

### eo
# translation by diestel@rzaix340.rz.uni-leipzig.de (Wolfram Diestel)
%package -n locales-eo
Summary: Base files for localization (Esperanto)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(eo): Bazaj dosieroj por lokaĵo (Esperanto)

%description -n locales-eo
These are the base files for Esperanto language localization; you need
it to correctly display 8bits esperanto characters, and for proper
alphabetical sorting and representation of dates and numbers according
to esperanto language conventions.

%description -n locales-eo -l eo
Tiuj ĉi estas la bazaj dosieroj por la esperantlingva lokaĵo; vi bezonas
ilin por ĝuste vidi 8-bitajn Esperanto-signojn kaj por ĝusta
alfabeta ordo, datindikoj kaj nombroj konvene al la konvencioj
en esperanta medio.

%post -n locales-eo
%{loc_add} eo_XX

%preun -n locales-eo
if [ "$1" = "0" ]; then
	%{loc_del} eo_XX
fi

%files -n locales-eo
%{_localedir}/eo_XX*

### es
%package -n locales-es
Summary: Base files for localization (Spanish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
#Summary(es): Ficheros de base para la localización (castellano)
Provides: locales-an = %{version}-%{release}

%description -n locales-es
These are the base files for Spanish language localization; you need
it to correctly display 8bits spanish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to spanish language conventions.

#%#description -n locales-es -l es
#Este paquete incluye las definiciones de locales para el castellano.
#Este paquete contiene lo necesario para la visualisación correcta de
#los caracteres 8bits del idioma español, para el orden alfabético 
#y para la representación correcta de los números y fechas según 
#las convenciones del castellano.

%post -n locales-es
%{loc_add} an_ES es_AR es_BO es_CL es_CO es_CR es_CU es_DO es_EC es_ES es_GT \
           es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US es_UY es_VE

%preun -n locales-es
if [ "$1" = "0" ]; then
	%{loc_del} an_ES es_AR es_BO es_CL es_CO es_CR es_DO es_EC es_ES es_CU \
                   es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US \
                   es_UY es_VE
fi

%files -n locales-es
%{_localedir}/es@tradicional
%{_localedir}/es_AR*
%{_localedir}/es_BO*
%{_localedir}/es_CL*
%{_localedir}/es_CO*
%{_localedir}/es_CR*
%{_localedir}/es_CU*
%{_localedir}/es_DO*
%{_localedir}/es_EC*
%{_localedir}/es_ES*
%{_localedir}/es_GT*
%{_localedir}/es_HN*
%{_localedir}/es_MX*
%{_localedir}/es_NI*
%{_localedir}/es_PA*
%{_localedir}/es_PE*
%{_localedir}/es_PR*
%{_localedir}/es_PY*
%{_localedir}/es_SV*
%{_localedir}/es_US*
%{_localedir}/es_UY*
%{_localedir}/es_VE*
# Aragonese
%{_localedir}/an_ES*

### et
# translation from: Ekke Einberg <ekke@data.ee>
%package -n locales-et
Summary: Base files for localization (Estonian)
Summary(et): Siin on vajalikud failid Linuxi eestindamiseks
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-et
These are the base files for Estonian language localization; you need
it to correctly display 8bits Estonian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Estonian language conventions.

%description -n locales-et -l et
Siin on vajalikud failid Linuxi eestindamiseks. Need on vajalikud
8-bitiliste eesti sümbolite
korrektseks esitamiseks ning õige tähestikulise järjestuse jaoks. Samuti
numbrite ja kuupäevade
eesti keele reeglitele vastavaks esituseks.

%post -n locales-et
%{loc_add} et_EE

%preun -n locales-et
if [ "$1" = "0" ]; then
	%{loc_del} et_EE
fi

%files -n locales-et
%{_localedir}/et_EE*

### eu
%package -n locales-eu
Summary: Base files for localization (Basque)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(eu): Euskarazko egokitzapenerako oinarrizko artxiboak
Summary(es): Archivos de base para la localización en euskara
Summary(fr): Fichiers de base pour la localisation en euskara (langue basque)

%description -n locales-eu
Linux-ek euskaraz badaki !
These are the base files for Basque language localization; you need
it to correctly display 8bits Basque characters, and for proper
representation of dates and numbers according to Basque language
conventions.

%description -n locales-eu -l eu
Linux-ek euskaraz badaki !
Hauek dira euskarazko egokitzapenerako oinarrizko artxiboak; euskarazko
8 biteko karaktereak zuzen ikusi ahal izateko zein zenbakiak
eta datak euskararen arauen arabera era egokian agertarazteko behar dira.

%description -n locales-eu -l es
Linux-ek euskaraz badaki !
Este paquete incluye las definiciones de locales para el euskara.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del euskara, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del euskara.

%description -n locales-eu -l fr
Ce paquet contient les définitions de locales en euskara batua.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%post -n locales-eu
%{loc_add} eu_ES

%preun -n locales-eu
if [ "$1" = "0" ]; then
	%{loc_del} eu_ES
fi

%files -n locales-eu
%{_localedir}/eu_ES*

### fa
%package -n locales-fa
Summary: Base files for localization (Farsi)
Summary(fa): پرونده‌های اساسی محلی‌سازی (فارسی)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-fa
These are the base files for Farsi language localization; you need
it to correctly display 8bits Farsi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Farsi language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%description -n locales-fa -l fa
اینها پرونده‌های اساسی زبان فارسی می‌باشند؛ شما برای نمایش درست ۸ بیت حروف فارسی، ترتیب مناسب الفبا، معرفی تاریخ و اعداد بر اساس قواعد زبان فارسی به آنها احتیاج دارید. توجه داشته باشید که این پاکت تعویض نگارش از راست به چپ و از چپ به راست را عهده‌دار نمی‌باشد و نه حتی ترکیب نهایی حروف را؛ این عمل را پایانه‌ی اکس، برنامه یا کارگزار کنسول مجازی انجام می‌دهند.

%post -n locales-fa
%{loc_add} fa_IR

%preun -n locales-fa
if [ "$1" = "0" ]; then
	%{loc_del} fa_IR
fi

%files -n locales-fa
%{_localedir}/fa_IR*

### fi
# translations by Jarkko Vaaraniemi <jvaarani@ees2.oulu.fi>
%package -n locales-fi
Summary: Base files for localization (Finnish)
Summary(fi): Tässä on perustiedot Linuxin suomentamiseen.
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-fi
These are the base files for Finnish language localization; you need
it to correctly display 8bits Finnish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Finnish language conventions.

%description -n locales-fi -l fi
Tässä on perustiedot Linuxin suomentamiseen. Tarvitset sitä suomalaisten
8-bittisten merkkien oikeaan esittämiseen, ja oikeaan aakkostamiseen ja
päivien ja numeroiden esitykseen suomenkielen käytännön mukaan.

%post -n locales-fi
%{loc_add} fi_FI

%preun -n locales-fi
if [ "$1" = "0" ]; then
	%{loc_del} fi_FI
fi

%files -n locales-fi
%{_localedir}/fi_FI*

### ff
%package	ff
Summary:	Base files for localization (Fulah)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	ff
These are the base files for Fulah language localization; you need
it to correctly display 8bits Fulah characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Fulah language conventions.

%post		ff
%{loc_add} ff_SN

%preun		ff
if [ "$1" = "0" ]; then
	%{loc_del} ff_SN
fi

%files		ff
%{_localedir}/ff_SN*

### fo
%package -n locales-fo
Summary: Base files for localization (Faroese)
Summary(fo): Hetta eru fílurnar tær tørvar til eina tillaging til føroyskt mál
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-fo
These are the base files for Faroese language localization; you need
it to correctly display 8bits Faroese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Faroese language conventions.

%description -n locales-fo -l fo
Hetta eru fílurnar tær tørvar til eina tillaging til føroyskt mál. Tær eru
neyðugar fyri at vísa føroyskar 8-bit stavir, fyri at fáa rætt stavrað og
vísa dagfestingar og tøl sambært føroyska siðvenju.

%post -n locales-fo
%{loc_add} fo_FO

%preun -n locales-fo
if [ "$1" = "0" ]; then
	%{loc_del} fo_FO
fi

%files -n locales-fo
%{_localedir}/fo_FO*

### fr
%package -n locales-fr
Summary: Base files for localization (French)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation (français)
Summary(de): Basisdateien für die Lokalisierung (Französisch)

%description -n locales-fr
These are the base files for French language localization; you need
it to correctly display 8bits french characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to french language conventions.

%description -n locales-fr -l fr
Ce paquet contient les définitions de locales en langue française.
Il permet aux applications de savoir quels caractères sont affichables
et donc afficher correctemment les caractères accentués et l'ordre
alphabetique; il contient aussi les definitions des representations
des dates des nombres et des symboles monétaires en Belgique, Canada,
Suisse, France et Luxembourg.

%description -n locales-fr -l de
Dies sind die Basisdateien für die französische Sprachanpassung; sie
werden für die korrekte Darstellung deutscher 8-Bit-Zeichen,
die französische Sortierreihenfolge sowie Datums- und Zahlendarstellung
benötigt.

%post -n locales-fr
%{loc_add} fr_BE fr_CA fr_CH fr_FR fr_LU

%preun -n locales-fr
if [ "$1" = "0" ]; then
	%{loc_del} fr_BE fr_CA fr_CH fr_FR fr_LU
fi

%files -n locales-fr
%{_localedir}/fr_BE*
%{_localedir}/fr_CA*
%{_localedir}/fr_CH*
%{_localedir}/fr_FR*
%{_localedir}/fr_LU*

### fur
%package -n locales-fur
Summary: Base files for localization (Friulan)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-fur
These are the base files for Friulan language localization; you need
it to correctly display 8bits friulan characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to friulan language conventions.

%post -n locales-fur
%{loc_add} fur_IT

%preun -n locales-fur
if [ "$1" = "0" ]; then
	%{loc_del} fur_IT
fi

%files -n locales-fur
%{_localedir}/fur_IT*

### fy
%package -n locales-fy
Summary: Base files for localization (Frisian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-fy
These are the base files for Frisian language localization; you need
it to correctly display 8bits frisian characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to frisian language conventions.

%post -n locales-fy
%{loc_add} fy_DE fy_NL

%preun -n locales-fy
if [ "$1" = "0" ]; then
	%{loc_del} fy_DE fy_NL
fi

%files -n locales-fy
%{_localedir}/fy_DE*
%{_localedir}/fy_NL*

### ga
%package -n locales-ga
Summary: Base files for localization (Irish)
Summary(ga): Bunchomaid do leagan áitiúil (Gaeilge)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ga
These are the base files for Irish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-ga -l ga
Seo iad na bunchomhaid do leagan áitiúil na Gaeilge; ní mór duit
iad a fháil chun tacar carachtar 8ngiotán a thaispeáint i gceart,
agus sórtáil in ord aibitre agus dátaí agus uimhreacha a chur i
láthair de réir coinbhinsiúnaigh na Gaeilge.

%post -n locales-ga
%{loc_add} ga_IE

%preun -n locales-ga
if [ "$1" = "0" ]; then
	%{loc_del} ga_IE
fi

%files -n locales-ga
%{_localedir}/ga_IE*

### gd
# translation by Caoimhin O Donnaile [caoimhin@SMO.UHI.AC.UK]
# and Cecil Ward [cecil.ward@FREE4ALL.CO.UK]
%package -n locales-gd
Summary: Base files for localization (Scottish Gaelic)
Summary(gd): Faidhlichean bunaiteach airson localization (Gaidhlig na h-Alba)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-gd
These are the base files for Scottish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-gd -l gd
Seo na faidhlichean bunaiteach air son "locale" na Gàidhlig.
Tha feum orra gus caractairean 8-bit fhaicinn, gus faclan a
chur ann an òrd na h-aibidile, agus gus àireamhan is cinn-latha
a riochdachadh a-réir nòs na Gàidhlig.

%post -n locales-gd
%{loc_add} gd_GB

%preun -n locales-gd
if [ "$1" = "0" ]; then
	%{loc_del} gd_GB
fi

%files -n locales-gd
%{_localedir}/gd_GB*

### gl
# translation from Emilio <nigrann@sandra.ctv.es>
%package -n locales-gl
Summary: Base files for localization (Galician)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(gl): Arquivos da base para definición de locais para o galego.
Summary(es): Archivos de base para la localización en idioma gallego

%description -n locales-gl
These are the base files for Galician language localization; you need
it to correctly display 8bits Galician characters, and for proper
representation of dates and numbers according to Galician language
conventions.

%description -n locales-gl -l gl
Este paquete inclúe as definicións de locais para o galego. Este paquete
contén o preciso para a representacion correcta dos caracteres de 8 bits
da fala galega, dos números e datas segundo as convencións do galego.

%description -n locales-gl -l es
Este paquete incluye las definiciones de locales para el gallego.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del gallego, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del gallego.

%post -n locales-gl
%{loc_add} gl_ES

%preun -n locales-gl
if [ "$1" = "0" ]; then
	%{loc_del} gl_ES
fi

%files -n locales-gl
%{_localedir}/gl_ES*

### gu
%package -n locales-gu
Summary: Base files for localization (Gujarati)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-gu
These are the base files for Gujarati language localization; you need
it to correctly display 8bits gujarati characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%post -n locales-gu
%{loc_add} gu_IN

%preun -n locales-gu
if [ "$1" = "0" ]; then
	%{loc_del} gu_IN
fi

%files -n locales-gu
%{_localedir}/gu_IN*

### gv
# translation by Brian Stowell <bstowell@MAILSERVICE.MCB.NET>
%package -n locales-gv
Summary: Base files for localization (Manx Gaelic)
Summary(gv): Coadanyn undinagh son ynnydaghey (Gaelg)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-gv
These are the base files for Manx Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-gv -l gv
T'ad shoh ny coadanyn undinagh ry-hoi ynnydaghey chengaghyn Gaelagh; ta
feme ayd orroo dy haishbyney karracteyryn Gaelagh 8-bit dy kiart, as son
reaghey-abbyrlit cooie as taishbyney-daaytyn as earrooyn coardail rish
reillyn-chengey Gaelagh.

%post -n locales-gv
%{loc_add} gv_GB

%preun -n locales-gv
if [ "$1" = "0" ]; then
	%{loc_del} gv_GB
fi

%files -n locales-gv
%{_localedir}/gv_GB*

### ha
%package -n locales-ha
Summary: Base files for localization (Hausa)
Group: System/Internationalization
#Icon: bulle-ha.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ha
These are the base files for Hausa language localization; you need
it to correctly display 8bits Hausa characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Hausa language conventions.

%post -n locales-ha
%{loc_add} ha_NG

%preun -n locales-ha
if [ "$1" = "0" ]; then
	%{loc_del} ha_NG
fi

%files -n locales-ha
%{_localedir}/ha_NG*

### he (formerly iw)
%package -n locales-he
Summary: Base files for localization (Hebrew)
Summary(he): המקום מכיל עמדות ללופויזציה בעברית 
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-he
These are the base files for Hebrew language localization; you need
it to correctly display 8bits Hebrew characters, and for proper
alfabetical sorting, and representation of dates and numbers 
according to Hebrew language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%description -n locales-he -l he
אלו הקבצים הבסיסיים לשימוש בעברית, אתה צריך את
החבילה הזאת בכדי להציג עברית של 8 ביטים,
לסידור לפי האלף בית, ולהצגה נכונה של מספרים
ותאריכים בהתאם ולקובל בשפה העברית. שים לב
שהחבילה הזאת אינה מטפטל בהמרה מימין לשמאל 
או משמאל לימין, על הישום או המסוף, בין אם של
X11 או המסוף וירטואלי, לעשות כן.

%post -n locales-he
%{loc_add} he_IL iw_IL

%preun -n locales-he
if [ "$1" = "0" ]; then
	%{loc_del} he_IL iw_IL
fi

%files -n locales-he
%{_localedir}/he_IL*
%{_localedir}/iw_IL*

### hi
%package -n locales-hi
Summary: Base files for localization (Hindi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-hi
These are the base files for Hindi language localization; you need
it to correctly display 8bits Hindi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Hindi language conventions.

%post -n locales-hi
%{loc_add} bho_IN brx_IN hi_IN ur_IN

%preun -n locales-hi
if [ "$1" = "0" ]; then
	%{loc_del} bho_IN brx_IN hi_IN ur_IN
fi

%files -n locales-hi
%{_localedir}/bho_IN*
%{_localedir}/brx_IN*
%{_localedir}/hi_IN*
%{_localedir}/ur_IN*

### hne
%package -n locales-hne
Summary: Base files for localization (Chhattisgarhi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-hne
These are the base files for Chhattisgarhi language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Chhattisgarhi language conventions.

%post -n locales-hne
%{loc_add} hne_IN

%preun -n locales-hne
if [ "$1" = "0" ]; then
	%{loc_del} hne_IN
fi

%files -n locales-hne
%{_localedir}/hne_IN

### hr
# translations by Vedran Rodic <vrodic@udig.hr>
%package -n locales-hr
Summary: Base files for localization (Croatian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(hr): Osnovne datoteke za lokalizaciju (Hrvatski)

%description -n locales-hr
These are the base files for Croatian language localization; you need
it to correctly display 8bits Croatian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Croatian language conventions.

%description -n locales-hr -l hr
Ovo su osnovne datoteke za lokalizaciju na Hrvatski jezik; potrebne su
da bi se pravilno prikazali 8 bitni Hrvatski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma i brojeva po pravilima
Hrvatskog jezika.

%post -n locales-hr
%{loc_add} hr_HR

%preun -n locales-hr
if [ "$1" = "0" ]; then
	%{loc_del} hr_HR
fi

%files -n locales-hr
%{_localedir}/hr_HR*

### hsb
%package -n locales-hsb
Summary: Base files for localization (Upper Sorbian)
Group: System/Internationalization
#Icon: bulle-hsb.xpm
Requires: locales = %{version}-%{release}

%description -n locales-hsb
These are the base files for Upper Sorbian language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Upper Sorbian language conventions.

%post -n locales-hsb
%{loc_add} hsb_DE

%preun -n locales-hsb
if [ "$1" = "0" ]; then
	%{loc_del} hsb_DE
fi

%files -n locales-hsb
%{_localedir}/hsb_DE*

### ht
%package -n locales-ht
Summary: Base files for localization (Breyol)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ht
These are the base files for Breyol language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Breyol language conventions.

%post -n locales-ht
%{loc_add} ht_HT

%preun -n locales-ht
if [ "$1" = "0" ]; then
	%{loc_del} ht_HT
fi

%files -n locales-ht
%{_localedir}/ht_HT

### hu
%package -n locales-hu
Summary: Base files for localization (Hungarian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(hu): Szükséges fájlok a magyarításhoz

%description -n locales-hu
These are the base files for Hungarian language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Hungarian language conventions.

%description -n locales-hu -l hu
Ezek a szükséges fájlok a magyarításhoz. Szükség van rá a
magyar helyesírás szabályainak megfelelő sorbarendezéshez,
számok és dátumok megjelenítéséhez.

%post -n locales-hu
%{loc_add} hu_HU

%preun -n locales-hu
if [ "$1" = "0" ]; then
	%{loc_del} hu_HU
fi

%files -n locales-hu
%{_localedir}/hu_HU*

### hy
# translations by Eugene Sevinian <sevinian@crdlx2.yerphi.am>
%package -n locales-hy
Summary: Base files for localization (Armenian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(hy): Ամփոփում. Հայացման հիմնական փաթեթները (ֆայլերը)

%description -n locales-hy
These are the base files for Armenian language localization.
You need it to correctly display 8bit Armenian chars, 
for sorting order and proper representation of dates and
numbers according to Armenian language conventions.

%description -n locales-hy -l hy
Այստեղ ներկայացված են հայացման հիմնական փաթեթները (ֆայլերը)։
Դրանք անհրաժեշտ են տվյալների ճշգրիտ խմբավորման եւ ամսաթվերի ու
թվային արժեքների պատշաճ ներկայցման համար համաձայն հայոց լեզվի
կանոնների։

%post -n locales-hy
%{loc_add} hy_AM

%preun -n locales-hy
if [ "$1" = "0" ]; then
	%{loc_del} hy_AM
fi

%files -n locales-hy
%{_localedir}/hy_AM*

### id (formerly in)
# translations by Mohammad DAMT <mdamt@cakraweb.com>
%package -n locales-id
Summary: Base files for localization (Indonesian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(id): File Utama untuk lokalisasi (dalam Bahasa Indonesia)

%description -n locales-id
These are the base files for Indonesian language localization.
You need it to correctly display sort, for proper representation
of dates and numbers according to Indonesian language conventions.

%description -n locales-id -l id
Ini adalah file untuk lokalisasi sistem ke dalam Bahasa Indonesia.
File ini dibutuhkan bila Anda ingin menampilkan tanggal dan penomoran
yang sesuai dengan kaidah Bahasa Indonesia.

%post -n locales-id
%{loc_add} id_ID

%preun -n locales-id
if [ "$1" = "0" ]; then
	%{loc_del} id_ID
fi

%files -n locales-id
%{_localedir}/id_ID*

### ig
%package -n locales-ig
Summary: Base files for localization (Igbo)
Group: System/Internationalization
#Icon: bulle-ig.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ig
These are the base files for Igbo language localization; you need
it to correctly display 8bits Igbo characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Igbo language conventions.

%post -n locales-ig
%{loc_add} ig_NG

%preun -n locales-ig
if [ "$1" = "0" ]; then
	%{loc_del} ig_NG
fi

%files -n locales-ig
%{_localedir}/ig_NG*

### ik
%package -n locales-ik
Summary: Base files for localization (Inupiaq)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ik
These are the base files for Inupiaq language localization; you need
it to correctly display 8bits Inupiac characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Inupiaq language conventions.

%post -n locales-ik
%{loc_add} ik_CA

%preun -n locales-ik
if [ "$1" = "0" ]; then
	%{loc_del} ik_CA
fi

%files -n locales-ik
%{_localedir}/ik_CA*

### is
# Gudmundur Erlingsson <gudmuner@lexis.hi.is>
%package -n locales-is
Summary: Base files for localization (Icelandic)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(is): Hér eru grunnskrár fyrir íslenska staðfærslu.

%description -n locales-is
These are the base files for Icelandic language localization; you need
it to correctly display 8bits Icelandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Icelandic language conventions.

%description -n locales-is -l is
Hér eru grunnskrár fyrir íslenska staðfærslu. Þú þarft á þessum skrám að
halda ef 8 bita séríslenskir stafir eiga að birtast réttir, til að fá
rétta stafrófsröð og til að dagsetningar og tölur birtist eins og
venja er í íslensku.

%post -n locales-is
%{loc_add} is_IS

%preun -n locales-is
if [ "$1" = "0" ]; then
	%{loc_del} is_IS
fi

%files -n locales-is
%{_localedir}/is_IS*

### it
%package -n locales-it
Summary: Base files for localization (Italian)
Summary(it): I files di base per l'adattamento della lingua italiana
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-it
These are the base files for Italian language localization; you need
it to correctly display 8bits Italian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Italian language conventions.

%description -n locales-it -l it
Questi sono i files di base per l'adattamento della lingua italiana. Vi
servono per visualizzare correttamente i caratteri a 8bit in italiano,
per l'ordinamento alfabetico corretto e per la rappresentazione delle
date e dei numeri in forma italiana.

%post -n locales-it
%{loc_add} it_CH it_IT

%preun -n locales-it
if [ "$1" = "0" ]; then
	%{loc_del} it_CH it_IT
fi

%files -n locales-it
%{_localedir}/it_CH*
%{_localedir}/it_IT*

### iu
%package -n locales-iu
Summary: Base files for localization (Inuktitut)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-iu
These are the base files for Inuktitut language localization; you need
it to correctly display 8bits Inuktitut characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Inuktitut language conventions.

%post -n locales-iu
%{loc_add} iu_CA

%preun -n locales-iu
if [ "$1" = "0" ]; then
	%{loc_del} iu_CA
fi

%files -n locales-iu
%{_localedir}/iu_CA*

### ja
# translation by "Evan D.A. Geisinger" <evan.geisinger@etak.com>
%package -n locales-ja
Summary: Base files for localization (Japanese)
Summary(ja): これは日本語ロカライゼーション用基礎ファイル集です。
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: libwcsmbs

%description -n locales-ja
These are the base files for Japanese language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to japanese language conventions.

%description -n locales-ja -l ja
これは日本語ロカライゼーション用基礎ファイル集です。これがないと，
７・８ビット文字コードの表示もできず、日本式日付き表現・数値表現ができない。
ただし、要注意点として：１６ビット文字コードが使えなかったので、
このロカール（地域特有設定データ集）が完璧・正式に「正確」とはいいきれない。
（多少「誤魔化し」を利かせて作ったからです）。

%post -n locales-ja
%{loc_add} ja_JP

%preun -n locales-ja
if [ "$1" = "0" ]; then
	%{loc_del} ja_JP
fi

%files -n locales-ja
%{_localedir}/ja_JP*

### ka
%package -n locales-ka
Summary: Base files for localization (Georgian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(ka): საბაზო ფაილები ქართულის ლოკალიზებისათვის.

%description -n locales-ka
These are the base files for Georgian language localization; you need
it to correctly display 8bits Georgian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Georgian language conventions.

%description -n locales-ka -l ka
საბაზო ფაილები ქართულის ლოკალიზებისათვის.
საჭიროა 8 ბიტიანი ფონტებით ქართული ანბანის სწორი ჩვენებისა
და სორტირებისათვის. აგრეთვე - თარიღის, ფულის ნიშნებისა და
რიცხვითი მნიშვნელობების მართებული წარმოდგენისათვის.

%post -n locales-ka
%{loc_add} ka_GE

%preun -n locales-ka
if [ "$1" = "0" ]; then
	%{loc_del} ka_GE
fi

%files -n locales-ka
%{_localedir}/ka_GE*

### kk
%package -n locales-kk
Summary: Base files for localization (Kazakh)
Group: System/Internationalization
#Icon: bulle-kk.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kk
These are the base files for Kazakh language localization; you need
it to correctly display 8bits Kazakh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kazakh language conventions.

%post -n locales-kk
%{loc_add} kk_KZ

%preun -n locales-kk
if [ "$1" = "0" ]; then
	%{loc_del} kk_KZ
fi

%files -n locales-kk
%{_localedir}/kk_KZ*

### kl
%package -n locales-kl
Summary: Base files for localization (Greenlandic)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-kl
These are the base files for Greenlandic language localization; you need
it to correctly display 8bits Greenlandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Grenlandic language conventions.

%post -n locales-kl
%{loc_add} kl_GL

%preun -n locales-kl
if [ "$1" = "0" ]; then
	%{loc_del} kl_GL
fi

%files -n locales-kl
%{_localedir}/kl_GL*

### km
%package -n locales-km
Summary: Base files for localization (Khmer)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-km
These are the base files for Khmer language localization; you need
it to correctly display 8bits Khmer characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Khmer language conventions.

%post -n locales-km
%{loc_add} km_KH

%preun -n locales-km
if [ "$1" = "0" ]; then
	%{loc_del} km_KH
fi

%files -n locales-km
%{_localedir}/km_KH*

### kn
%package -n locales-kn
Summary: Base files for localization (Kannada)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-kn
These are the base files for Kannada language localization; you need
it to correctly display 8bits Kannada characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kannada language conventions.

%post -n locales-kn
%{loc_add} kn_IN

%preun -n locales-kn
if [ "$1" = "0" ]; then
	%{loc_del} kn_IN
fi

%files -n locales-kn
%{_localedir}/kn_IN*

### ko
# translation by Soo-Jin Lee <NothingSpecial@rocketmail.com>
%package -n locales-ko
Summary: Base files for localization (Korean)
Summary(ko): 이것들은 한국어에만 국한된 기초화일들이다
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: libwcsmbs

%description -n locales-ko
These are the base files for Korean language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to korean language conventions.

%description -n locales-ko -l ko
이것들은 한국어에만 국한된 기초화일들이다 당신은 한국어규정에
의한 적절한 날짜와 숫자들의 표시를 8바이트와 7바이트의 한국어
코드로 정확히 배열하는데 그것이 필요하다.

%post -n locales-ko
%{loc_add} ko_KR

%preun -n locales-ko
if [ "$1" = "0" ]; then
	%{loc_del} ko_KR
fi

%files -n locales-ko
%{_localedir}/ko_KR*

### kok
%package -n locales-kok
Summary: Base files for localization (Konkani)
Group: System/Internationalization
#Icon: bulle-kk.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kok
These are the base files for Konkani language localization; you need
it to correctly display 8bits Konkani characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Konkani language conventions.

%post -n locales-kok
%{loc_add} kok_IN

%preun -n locales-kok
if [ "$1" = "0" ]; then
	%{loc_del} kok_IN
fi

%files -n locales-kok
%{_localedir}/kok_IN*

### ks
%package -n locales-ks
Summary: Base files for localization (Kashmiri)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ks
These are the base files for Kashmiri language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Kashmiri language conventions.

%post -n locales-ks
%{loc_add} ks_IN ks_IN@devanagari

%preun -n locales-ks
if [ "$1" = "0" ]; then
	%{loc_del} ks_IN ks_IN@devanagari
fi

%files -n locales-ks
%{_localedir}/ks_IN
%{_localedir}/ks_IN@devanagari

### ku
%package -n locales-ku
Summary: Base files for localization (Kurdish)
Summary(ku): Rûpel-tâmar ji bo naskirinâ cîh (Kurdi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ku
These are the base files for Kurdish language localization; you need
it to correctly display 8bits Kurdish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kurdish language conventions.

%description -n locales-ku -l ku
Vâhan rûpelen-tâmarê ji bo cîhnaskirînâ zîmanê kurdi, ji bo qû herfên
kurd â 8bits ân vêrin ditin, vâ rûpel-tamar bî vê gêrege ji bo alfabêya
kurdi, dîrok, seat, hêjmar û edetê malbatâ zîmanê kurdin vêre naskirin
bi haliyê systême

%post -n locales-ku
%{loc_add} ku_TR

%preun -n locales-ku
if [ "$1" = "0" ]; then
	%{loc_del} ku_TR
fi

%files -n locales-ku
%{_localedir}/ku_TR*

### kw
# translations by Andrew Climo-Thompson <andrew@clas.demon.co.uk>
# Laurie Climo <lj.climo@ukonline.co.uk> & Marion Gunn <mgunn@ucd.ie>
%package -n locales-kw
Summary: Base files for localization (Cornish)
Summary(kw): Fylennow sel dhe gernewekhe
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-kw
These are the base files for Cornish language localization; you need
it to correctly display 8bits cornish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Cornish language conventions.

%description -n locales-kw -l kw
Otomma'n fylennow sel dhe Gernewekhe an system; 'ma ethom anodho
dhe dhysplegya lythrennow Kernewek 8-ryf dhe wyr, ha sortya yn ordyr
abecedery gwyw ha dysquesdhes dedhyow ha nyverow herwyth rewlys
a'n tavas Kernewek.

%post -n locales-kw
%{loc_add} kw_GB

%preun -n locales-kw
if [ "$1" = "0" ]; then
	%{loc_del} kw_GB
fi

%files -n locales-kw
%{_localedir}/kw_GB*

### ky
%package -n locales-ky
Summary: Base files for localization (Kyrgyz)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ky
These are the base files for Kyrgyz language localization; you need
it to correctly display 8bits kyrgyz characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kyrgyz language conventions.

%post -n locales-ky
%{loc_add} ky_KG

%preun -n locales-ky
if [ "$1" = "0" ]; then
	%{loc_del} ky_KG
fi

%files -n locales-ky
%{_localedir}/ky_KG*

### lb
%package	lb
Summary:	Base files for localization (Luxembourgish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	lb
These are the base files for Luxembourgish language localization; you need
it to correctly display 8bits Luxembourgish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Luxembourgish language conventions.

%post		lb
%{loc_add} lb_LU

%preun		lb
if [ "$1" = "0" ]; then
	%{loc_del} lb_LU
fi

%files		lb
%{_localedir}/lb_LU*

### lg
%package -n locales-lg
Summary: Base files for localization (Luganda)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-lug = %{version}-%{release}

%description -n locales-lg
These are the base files for Luganda (Ganda) language localization; you need
it to correctly display 8bits Luganda characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Luganda language conventions.

%post -n locales-lg
%{loc_add} lg_UG

%preun -n locales-lg
if [ "$1" = "0" ]; then
	%{loc_del} lg_UG
fi

%files -n locales-lg
%{_localedir}/lg_UG*

### li
%package -n locales-li
Summary: Base files for localization (Limburguish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-li
These are the base files for Limburguish language localization; you need
it to correctly display 8bits characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Limburguish language conventions.

%post -n locales-li
%{loc_add} li_BE li_NL

%preun -n locales-li
if [ "$1" = "0" ]; then
	%{loc_del} li_BE li_NL
fi

%files -n locales-li
%{_localedir}/li_BE*
%{_localedir}/li_NL*

### lij
%package	lij
Summary:	Base files for localization (Ligurian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	lij
These are the base files for Ligurian language localization; you need
it to correctly display 8bits Ligurian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Ligurian language conventions.

%post		lij
%{loc_add} lij_IT

%preun		lij
if [ "$1" = "0" ]; then
	%{loc_del} lij_IT
fi

%files		lij
%{_localedir}/lij_IT*

### lo
%package -n locales-lo
Summary: Base files for localization (Laotian) [INCOMPLETE]
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-lo
These are the base files for Laotian language localization; you need
it to correctly display 8bits lao characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Laotian language conventions.

%post -n locales-lo
%{loc_add} lo_LA

%preun -n locales-lo
if [ "$1" = "0" ]; then
	%{loc_del} lo_LA
fi

%files -n locales-lo
%{_localedir}/lo_LA*

### lt
%package -n locales-lt
Summary: Base files for localization (Lithuanian)
Summary(lt): Failai skirti lokalės lituanizacijai
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-lt
These are the base files for Lithuanian language localization; you need
it to correctly display 8bits Lithuanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Lithuanian language conventions.

%description -n locales-lt -l lt
Baziniai failai skirti lokalės lituanizacijai; reikalingi korektiš
kam lietuviškų, 8 bitų simbolių atvaizdavimui, alfabetiniam rūšiavimui
bei datos ir skaičių atvaizdavimui.

%post -n locales-lt
%{loc_add} lt_LT

%preun -n locales-lt
if [ "$1" = "0" ]; then
	%{loc_del} lt_LT
fi

%files -n locales-lt
%{_localedir}/lt_LT*

### lv
# translation done by Vitauts Stochka <vit@dpu.lv>
%package -n locales-lv
Summary: Base files for localization (Latvian)
Summary(lv): Lokalizācijas pamatfaili (Latviešu)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-lv
These are the base files for Latvian language localization; you need
it to correctly display 8bits Latvian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Latvian language conventions.


%description -n locales-lv -l lv
Šie ir latviešu valodas lokalizācijas pamatfaili; tie jums ir
nepieciešami, lai pareizi attēlotu 8bitu latviešu burtus, veiktu
pareizu kārtošanu pēc alfabēta, kā arī attēlotu datumus un skaitļus
saskaņā ar latviešu valodā pieņemtajām normām.

%post -n locales-lv
%{loc_add} lv_LV

%preun -n locales-lv
if [ "$1" = "0" ]; then
	%{loc_del} lv_LV
fi

%files -n locales-lv
%{_localedir}/lv_LV*

### mag
%package -n locales-mag
Summary: Base files for localization (Magahi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mag
These are the base files for Magahi language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Magahi language conventions.

%post -n locales-mag
%{loc_add} mag_IN

%preun -n locales-mag
if [ "$1" = "0" ]; then
	%{loc_del} mag_IN
fi

%files -n locales-mag
%{_localedir}/mag_IN

### mai
%package -n locales-mai
Summary: Base files for localization (Maithili)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mai
These are the base files for Maithili language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Maithili language conventions.

%post -n locales-mai
%{loc_add} mai_IN

%preun -n locales-mai
if [ "$1" = "0" ]; then
	%{loc_del} mai_IN
fi

%files -n locales-mai
%{_localedir}/mai_IN

### mg
%package -n locales-mg
Summary: Base files for localization (Malagasy)
Group: System/Internationalization
#Icon: bulle-mg.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mg
These are the base files for Malagasy language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Malagasy language conventions.

%post -n locales-mg
%{loc_add} mg_MG

%preun -n locales-mg
if [ "$1" = "0" ]; then
	%{loc_del} mg_MG
fi

%files -n locales-mg
%{_localedir}/mg_MG*

### mhr
%package	mhr
Summary:	Base files for localization (Mari)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	mhr
These are the base files for Mari language localization; you need
it to correctly display 8bits Mari characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Mari language conventions.

%post		mhr
%{loc_add} mhr_RU

%preun		mhr
if [ "$1" = "0" ]; then
	%{loc_del} mhr_RU
fi

%files		mhr
%{_localedir}/mhr_RU*


### mi
# Maori translation provided by Gasson <gasson@clear.net.nz>
%package -n locales-mi
Summary: Base files for localization (Maori)
Summary(mi): Ko ngā kōnae papa mō te whakaā-rohe (Māori)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mi
These are the base files for Maori language localization; you need it for
it to correctly display 8bits Maori characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Maori language conventions.

%description -n locales-mi -l mi
Ko ēnei ngā kōnae papa mō te whakaā-rohe reo Maori; he mea kē tēnei kei
whakaatuhia i ngā pū Māori mati kaupapa-ā-rua e waru kia tika ai, ā, mō te
whakatakotoranga hoki o ngā wā me ngā nama kia tika ai anō e ai ki ngā aro
whānui reo Māori.

%post -n locales-mi
%{loc_add} mi_NZ

%preun -n locales-mi
if [ "$1" = "0" ]; then
	%{loc_del} mi_NZ
fi

%files -n locales-mi
%{_localedir}/mi_NZ*

### mk
%package -n locales-mk
Summary: Base files for localization (Macedonian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mk
These are the base files for Macedonian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Macedonian language conventions.

%post -n locales-mk
%{loc_add} mk_MK

%preun -n locales-mk
if [ "$1" = "0" ]; then
	%{loc_del} mk_MK
fi

%files -n locales-mk
%{_localedir}/mk_MK*

### ml
%package -n locales-ml
Summary: Base files for localization (Malayalam)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ml
These are the base files for Malayalam language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malayalam language conventions.

%post -n locales-ml
%{loc_add} ml_IN

%preun -n locales-ml
if [ "$1" = "0" ]; then
	%{loc_del} ml_IN
fi

%files -n locales-ml
%{_localedir}/ml_IN*

### mn
%package -n locales-mn
Summary: Base files for localization (Mongolian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mn
These are the base files for Mongolian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Mongolian language conventions.

%post -n locales-mn
%{loc_add} mn_MN

%preun -n locales-mn
if [ "$1" = "0" ]; then
	%{loc_del} mn_MN
fi

%files -n locales-mn
%{_localedir}/mn_MN*

### mni
%package -n locales-mni
Summary: Base files for localization (Manipuri)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mni
These are the base files for Manipuri language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Manipuri language conventions.

%post -n locales-mni
%{loc_add} mni_IN

%preun -n locales-mni
if [ "$1" = "0" ]; then
	%{loc_del} mni_IN
fi

%files -n locales-mni
%{_localedir}/mni_IN

### mr
%package -n locales-mr
Summary: Base files for localization (Marathi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mr
These are the base files for Marathi language localization; you need
it to correctly display 8bits Marathi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Marathi language conventions.

%post -n locales-mr
%{loc_add} mr_IN

%preun -n locales-mr
if [ "$1" = "0" ]; then
	%{loc_del} mr_IN
fi

%files -n locales-mr
%{_localedir}/mr_IN*

### ms
%package -n locales-ms
Summary: Base files for localization (Malay)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ms
These are the base files for Malay language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malay language conventions.

%post -n locales-ms
%{loc_add} ms_MY

%preun -n locales-ms
if [ "$1" = "0" ]; then
	%{loc_del} ms_MY
fi

%files -n locales-ms
%{_localedir}/ms_MY*

### mt
# translation by Ramon Casha <rcasha@waldonet.net.mt>
%package -n locales-mt
Summary: Base files for localization (Maltese)
Summary(mt): Files ewlenin għat-traduzzjoni (Maltin)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-mt
These are the base files for Maltese language localization; you need
it to correctly display 8bits Maltese characters, and for proper
alphabetical sorting and representation of dates and numbers according\
to Maltese language conventions.

%description -n locales-mt -l mt
Dawn huma l-files ewlenin għat-traduzzjoni għal-lingwa Maltija;
għandek bżonnhom biex turi l-ittri 8-bit Maltin sew, biex tissortja
alfabetikament, u biex turi dati u numri skond il-konvenzjonijiet
tal-lingwa Maltija.

%post -n locales-mt
%{loc_add} mt_MT

%preun -n locales-mt
if [ "$1" = "0" ]; then
	%{loc_del} mt_MT
fi

%files -n locales-mt
%{_localedir}/mt_MT*

### my
%package -n locales-my
Summary: Base files for localization (Burmese)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-my
These are the base files for Burmese language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Burmese language conventions.

%post -n locales-my
%{loc_add} my_MM

%preun -n locales-my
if [ "$1" = "0" ]; then
	%{loc_del} my_MM
fi

%files -n locales-my
%{_localedir}/my_MM

### nds
%package -n locales-nds
Summary: Base files for localization (Lower Saxon)
Summary(de): Basisdateien für die Lokalisierung (Plautdietsch)
Summary(nds): Grundspikjaloden fe' Sproaktoopaussinj (Plautdietsch)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-nds
These are the base files for Lower Saxon language
localization; you need it to correctly display 8bits Lower Saxon characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Lower Saxon language conventions.

%description -n locales-nds -l nds
Dit send de Grundspikjaloden fe' de plautdietsche Sproaktoopaussinj.
Dee woaren jebrukt om de 8-bit'sche plautdietsche Teakjens noh Droat
ut to drekjen, aules jescheit noh'm Aulfabeet to sortieren, un uk de Dotums
un Nummasch soo auntojäwen soo's daut jeweehnlich em Plautdietschen jeiht.

%description -n locales-nds -l de
Dies sind die Basisdateien für die plautdietsche Sprachanpassung; sie
werden für die korrekte Darstellung plautdietscher 8-Bit-Zeichen,
die plautdietsche Sortierreihenfolge sowie Datums- und Zahlendarstellung
benötigt

%post -n locales-nds
%{loc_add} nds_DE nds_NL

%preun -n locales-nds
if [ "$1" = "0" ]; then
	%{loc_del} nds_DE nds_NL
fi

%files -n locales-nds
%{_localedir}/nds_DE*
%{_localedir}/nds_NL*

### ne
%package -n locales-ne
Summary: Base files for localization (Nepali)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ne
These are the base files for Nepali language localization; you need
it to correctly display 8bits Nepali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Nepali language conventions.

%post -n locales-ne
%{loc_add} ne_NP

%preun -n locales-ne
if [ "$1" = "0" ]; then
	%{loc_del} ne_NP
fi

%files -n locales-ne
%{_localedir}/ne_NP*

### nl
%package -n locales-nl
Summary: Base files for localization (Dutch)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue néerlandaise
Summary(nl): Dit zijn de basisbestanden nodig voor de Nederlandse taal

%description -n locales-nl
These are the base files for Dutch language localization; you need
it to correctly display 8bits Dutch characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Dutch language conventions.

%description -n locales-nl -l fr
Ce paquet contient les définitions de locales en langue néerlandaise.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%description -n locales-nl -l nl
Dit zijn de basisbestanden nodig voor de Nederlandse taalmodule; ze zijn
noodzakelijk om de 8bits Nederlandse karakters correct weer te geven en
voor een juiste alfabetische sortering en weergave van data en nummers
volgens de Nederlandse Taalconventies

%post -n locales-nl
%{loc_add} nl_AW nl_BE nl_NL

%preun -n locales-nl
if [ "$1" = "0" ]; then
	%{loc_del} nl_AW nl_BE nl_NL
fi

%files -n locales-nl
%{_localedir}/nl_AW*
%{_localedir}/nl_BE*
%{_localedir}/nl_NL*

### no
# translations by peter@datadok.no
%package -n locales-no
Summary: Base files for localization (Norwegian)
#Summary(nb): Dette er basisfilene for lokalisering til norsk språk
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-nn = %{version}-%{release}
Provides: locales-nb = %{version}-%{release}

%description -n locales-no
These are the base files for Norwegian language localization; you need
it to correctly display 8bits Norwegian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Norwegian language conventions.

#%#description -n locales-no -l nb
#Dette er basisfilene for lokalisering til norsk språk. Du trenger dette
#for å vise norske 8-bitstegn på riktig måte og for å få riktig sortering
#etter alfabetet og visning av datoer og tall i samsvar med norske
#konvensjoner.

%post -n locales-no
%{loc_add} nb_NO nn_NO

%preun -n locales-no
if [ "$1" = "0" ]; then
	%{loc_del} nb_NO nn_NO
fi

%files -n locales-no
%{_localedir}/nb_NO*
%{_localedir}/nn_NO*

### nr
%package -n locales-nr
Summary: Base files for localization (Ndebele)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-nr
These are the base files for Ndebele language localization; you need
it to correctly display 8bits Ndebele characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Ndebele language conventions.

%post -n locales-nr
%{loc_add} nr_ZA

%preun -n locales-nr
if [ "$1" = "0" ]; then
	%{loc_del} nr_ZA
fi

%files -n locales-nr
%{_localedir}/nr_ZA*

### nso
%package -n locales-nso
Summary: Base files for localization (Northern Sotho)
Group: System/Internationalization
#Icon: bulle-nso.xpm
Requires: locales = %{version}-%{release}

%description -n locales-nso
These are the base files for Northern Sotho language localization; you need
it to correctly display 8bits Northern Sotho characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Northern Sotho language conventions.

%post -n locales-nso
%{loc_add} nso_ZA

%preun -n locales-nso
if [ "$1" = "0" ]; then
	%{loc_del} nso_ZA
fi

%files -n locales-nso
%{_localedir}/nso_ZA*

### oc
%package -n locales-oc
Summary: Base files for localization (Occitan)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(oc): fichièrs de basa per localisar (occitan)

%description -n locales-oc
These are the base files for Occitan language localization; you need
it to correctly display 8bits Occitan characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Occitan language conventions.

%description -n locales-oc -l oc
Aicí avem empaquetat los fichièrs de basa per la lengua occitana : los
programas n'an de besonh per afichar corrèctament los caractèrs dins lo
fenestron, classar l'òrdre alfabetic e atanben comptar los jorns 
e los meses en occitan.

%post -n locales-oc
%{loc_add} oc_FR

%preun -n locales-oc
if [ "$1" = "0" ]; then
	%{loc_del} oc_FR
fi

%files -n locales-oc
%{_localedir}/oc_FR*

### or
%package -n locales-or
Summary: Base files for localization (Oriya)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-or
These are the base files for Oriya language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Oriya language conventions.

%post -n locales-or
%{loc_add} or_IN

%preun -n locales-or
if [ "$1" = "0" ]; then
	%{loc_del} or_IN
fi

%files -n locales-or
%{_localedir}/or_IN

### os
%package	os
Summary:	Base files for localization (Ossetian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	os
These are the base files for Ossetian language localization; you need
it to correctly display 8bits Ossetian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Ossetian language conventions.

%post		os
%{loc_add} os_RU

%preun		os
if [ "$1" = "0" ]; then
	%{loc_del} os_RU
fi

%files		os
%{_localedir}/os_RU*

### pa
%package -n locales-pa
Summary: Base files for localization (Punjabi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-pa
These are the base files for Punjabi localization; you need it to correctly
display 8bits characters, and for proper alphabetical sorting and
representation of dates and numbers according
to Punjabi language conventions.

%post -n locales-pa
%{loc_add} pa_IN pa_PK

%preun -n locales-pa
if [ "$1" = "0" ]; then
	%{loc_del} pa_IN pa_PK
fi

%files -n locales-pa
%{_localedir}/pa_IN*
%{_localedir}/pa_PK*

### pap
%package -n locales-pap
Summary: Base files for localization (Papiamento)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: locales-pp
Provides: locales-pp = %{version}-%{release}

%description -n locales-pap
These are the base files for Papiamento language localization; you need
it to correctly display 8bits Papiamento characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Papiamento language conventions.

%post -n locales-pap
%{loc_add} pap_AN

%preun -n locales-pap
if [ "$1" = "0" ]; then
	%{loc_del} pap_AN
fi

%files -n locales-pap
%{_localedir}/pap_AN*

### pl
%package	pl
Summary:	Base files for localization (Polish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	pl
These are the base files for Polish language localization; you need
it to correctly display 8bits Polish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Polish language conventions.

%post		pl
%{loc_add} csb_PL pl_PL

%preun		pl
if [ "$1" = "0" ]; then
	%{loc_del} csb_PL pl_PL
fi

%files		pl
%{_localedir}/csb_PL*
%{_localedir}/pl_PL*

### ps
%package -n locales-ps
Summary: Base files for localization (Pashto)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ps
These are the base files for Pashto language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Pashto language conventions.

%post -n locales-ps
%{loc_add} ps_AF

%preun -n locales-ps
if [ "$1" = "0" ]; then
	%{loc_del} ps_AF
fi

%files -n locales-ps
%{_localedir}/ps_AF

### pt
%package -n locales-pt
Summary: Base files for localization (Portuguese)
#Summary(pt): Estes são os arquivos básicos para a localização (Português)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-pt_BR = %{version}-%{release}
Provides: locales-pt_PT = %{version}-%{release}

%description -n locales-pt
These are the base files for Portuguese language localization; you need
it to correctly display 8bits Portuguese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Portuguese language conventions.

#%#description -n locales-pt -l pt
#Estes são os arquivos básicos para a localização lingüística em português;
#eles são necessários para que o sistema mostre corretamente caracteres
#portugueses de 8 bits, e para que tenha as apropriadas ordenações
#alfabéticas e representação de datas e números de acordo com as convenções
#da língua portuguesa.

%post -n locales-pt
%{loc_add} pt_BR pt_PT

%preun -n locales-pt
if [ "$1" = "0" ]; then
	%{loc_del} pt_BR pt_PT
fi

%files -n locales-pt
%{_localedir}/pt_BR*
%{_localedir}/pt_PT*

### ro
# translation from "Mihai" <mihai@ambra.ro>
%package -n locales-ro
Summary: Base files for localization (Romanian)
Summary(ro): Acestea sînt fisierele pentru române localizarea
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ro
These are the base files for Romanian language localization; you need
it to correctly display 8bits Romanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Romanian language conventions.

%description -n locales-ro -l ro
Acestea sînt fisierele de baza pentru localizarea în limba româna; sînt
necesare pentru afisarea corecta a caracterelor românesti pe 8 biti precum
si pentru sortarea alfabetica si reprezentarea datelor si numerelor conform
cu conventiile din limba româna.

%post -n locales-ro
%{loc_add} ro_RO

%preun -n locales-ro
if [ "$1" = "0" ]; then
	%{loc_del} ro_RO
fi

%files -n locales-ro
%{_localedir}/ro_RO*

### ru
%package -n locales-ru
Summary: Base files for localization (Russian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(ru): Основные файлы региональных установок (для России)

%description -n locales-ru
These are the base files for Russian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Russian language conventions.

%description -n locales-ru -l ru
Эти файлы содержат основные региональные установки
для русского языка; они необходимы для правильного
представления 8-битных букв кириллицы на экране,
для правильной алфавитной сортировки и для
представления дат и чисел в соответствии с правилами
русского языка.

%post -n locales-ru
%{loc_add} ru_RU ru_UA

%preun -n locales-ru
if [ "$1" = "0" ]; then
	%{loc_del} ru_RU ru_UA
fi

%files -n locales-ru
%{_localedir}/ru_RU*
%{_localedir}/ru_UA*

### rw
%package -n locales-rw
Summary: Base files for localization (Kinyarwanda)
Group: System/Internationalization
#Icon: bulle-rw.xpm
Requires: locales = %{version}-%{release}

%description -n locales-rw
These are the base files for Kinyarwanda language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kinyarwanda language conventions.

%post -n locales-rw
%{loc_add} rw_RW

%preun -n locales-rw
if [ "$1" = "0" ]; then
	%{loc_del} rw_RW
fi

%files -n locales-rw
%{_localedir}/rw_RW*

### sa
%package -n locales-sa
Summary: Base files for localization (Sanskrit)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sa
These are the base files for Sanskrit language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Sanskrit language conventions.

%post -n locales-sa
%{loc_add} sa_IN

%preun -n locales-sa
if [ "$1" = "0" ]; then
	%{loc_del} sa_IN
fi

%files -n locales-sa
%{_localedir}/sa_IN

### sat
%package -n locales-sat
Summary: Base files for localization (Santali)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sat
These are the base files for Santali language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Santali language conventions.

%post -n locales-sat
%{loc_add} sat_IN

%preun -n locales-sat
if [ "$1" = "0" ]; then
	%{loc_del} sat_IN
fi

%files -n locales-sat
%{_localedir}/sat_IN

### sc
%package -n locales-sc
Summary: Base files for localization (Sardinian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sc
These are the base files for Sardinian language localization; you need
it to correctly display 8bits sardinian characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to sardinian language conventions.

%post -n locales-sc
%{loc_add} sc_IT

%preun -n locales-sc
if [ "$1" = "0" ]; then
	%{loc_del} sc_IT
fi

%files -n locales-sc
%{_localedir}/sc_IT*

### sd
%package -n locales-sd
Summary: Base files for localization (Sindhi)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sd
These are the base files for Sindhi language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Sindhi language conventions.

%post -n locales-sd
%{loc_add} sd_IN sd_IN@devanagari

%preun -n locales-sd
if [ "$1" = "0" ]; then
	%{loc_del} sd_IN sd_IN@devanagari
fi

%files -n locales-sd
%{_localedir}/sd_IN
%{_localedir}/sd_IN@devanagari

### se
%package -n locales-se
Summary: Base files for localization (Saami)
Group: System/Internationalization
#Icon: bulle-se.xpm
Requires: locales = %{version}-%{release}

%description -n locales-se
These are the base files for Saami language localization; you need
it to correctly display 8bits Saami characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Saami language conventions.

%post -n locales-se
%{loc_add} se_NO

%preun -n locales-se
if [ "$1" = "0" ]; then
	%{loc_del} se_NO
fi

%files -n locales-se
%{_localedir}/se_NO*

### shs
%package -n locales-shs
Summary: Base files for localization (Secwepemctsin)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-shs
These are the base files for Secwepemctsin language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Secwepemctsin language conventions.

%post -n locales-shs
%{loc_add} shs_CA

%preun -n locales-shs
if [ "$1" = "0" ]; then
	%{loc_del} shs_CA
fi

%files -n locales-shs
%{_localedir}/shs_CA

### si
%package -n locales-si
Summary: Base files for localization (Sinhala)
Group: System/Internationalization
#Icon: bulle-si.xpm
Requires: locales = %{version}-%{release}

%description -n locales-si
These are the base files for Sinhala language localization; you need
it to correctly display 8bits sardinian characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to sinhalese language conventions.

%post -n locales-si
%{loc_add} si_LK

%preun -n locales-si
if [ "$1" = "0" ]; then
	%{loc_del} si_LK
fi

%files -n locales-si
%{_localedir}/si_LK*

### sk
%package -n locales-sk
Summary: Base files for localization (Slovak)
Summary(sk): Toto su zakladne súbory pre slovenskú lokalizaciu
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sk
These are the base files for Slovak language localization; you need
it to correctly display 8bits Slovak characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovak language conventions.

%description -n locales-sk -l sk
Tu sú súbory potrebné pre správnu slovenskú lokalizáciu; potrebujete ich pre
korektné zobrazovanie slovenských 8bitových znakov a pre správne triedenie a
reprezentáciu dátumu a čísel podľa konvencií slovenského jazyka.

%post -n locales-sk
%{loc_add} sk_SK

%preun -n locales-sk
if [ "$1" = "0" ]; then
	%{loc_del} sk_SK
fi

%files -n locales-sk
%{_localedir}/sk_SK*

### sl
# Translations from Roman Maurer <roman.maurer@fmf.uni-lj.si>
%package -n locales-sl
Summary: Base files for localization (Slovenian)
Summary(sl): Osnovne datoteke za lokalizacijo (slovenščina)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sl
These are the base files for Slovenian language localization; you need
it to correctly display 8bits Slovenian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovenian language conventions.

%description -n locales-sl -l sl
To so osnovne datoteke za lokalizacijo Linuxa na slovenski
jezik; potrebujete jih za pravilni prikaz 8-bitnih
slovenskih znakov in za pravilno urejanje po abecedi ter
predstavitev datumov in številk glede na pravila
slovenskega jezika.

%post -n locales-sl
%{loc_add} sl_SI

%preun -n locales-sl
if [ "$1" = "0" ]; then
	%{loc_del} sl_SI
fi

%files -n locales-sl
%{_localedir}/sl_SI*

### sr
%package	sr
Summary:	Base files for localization (Serbian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	sr
These are the base files for Serbian language localization; you need
it to correctly display 8bits Serbian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Serbian language conventions.

%post		sr
%{loc_add} sr_ME sr_RS

%preun		sr
if [ "$1" = "0" ]; then
	%{loc_del} sr_ME sr_RS
fi

%files		sr
%{_localedir}/sr_ME*
%{_localedir}/sr_RS*

### so
%package -n locales-so
Summary: Base files for localization (Somali)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-so
These are the base files for Somali language localization; you need
it to correctly display 8bits Somali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Somali language conventions.

%post -n locales-so
%{loc_add} so_DJ so_ET so_KE so_SO

%preun -n locales-so
if [ "$1" = "0" ]; then
	%{loc_del} so_DJ so_ET so_KE so_SO
fi

%files -n locales-so
%{_localedir}/so_DJ*
%{_localedir}/so_ET*
%{_localedir}/so_KE*
%{_localedir}/so_SO*

### sq
%package -n locales-sq
Summary: Base files for localization (Albanian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sq
These are the base files for Albanian language localization; you need
it to correctly display 8bits Albanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Albanian language conventions.

%post -n locales-sq
%{loc_add} sq_AL sq_MK

%preun -n locales-sq
if [ "$1" = "0" ]; then
	%{loc_del} sq_AL sq_MK
fi

%files -n locales-sq
%{_localedir}/sq_AL*
%{_localedir}/sq_MK*

### ss
%package -n locales-ss
Summary: Base files for localization (Swati)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ss
These are the base files for Swati language localization; you need
it to correctly display 8bits Swati characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Swati language conventions.

%post -n locales-ss
%{loc_add} ss_ZA

%preun -n locales-ss
if [ "$1" = "0" ]; then
	%{loc_del} ss_ZA
fi

%files -n locales-ss
%{_localedir}/ss_ZA*

### st
%package -n locales-st
Summary: Base files for localization (Sotho)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-st
These are the base files for Sotho language localization; you need
it to correctly display 8bits Sotho characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Sotho language conventions.

%post -n locales-st
%{loc_add} st_ZA

%preun -n locales-st
if [ "$1" = "0" ]; then
	%{loc_del} st_ZA
fi

%files -n locales-st
%{_localedir}/st_ZA*

### sv
# translation by Erik Almqvist <erik.almqvist@vrg.se>
%package -n locales-sv
Summary: Base files for localization (Swedish)
Summary(sv): Detta är huvudfilerna för svenskt språkstöd
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sv
These are the base files for Swedish language localization; you need
it to correctly display 8bits Swedish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swedish language conventions.

%description -n locales-sv -l sv
Detta är huvudfilerna för svenskt språkstöd. De behövs för att korrekt visa
svenska 8 bitars tecken och för korrekt alfabetisk sortering. De gör även
att datum och nummerformat visas på svenskt vis.

%post -n locales-sv
%{loc_add} sv_FI sv_SE

%preun -n locales-sv
if [ "$1" = "0" ]; then
	%{loc_del} sv_FI sv_SE
fi

%files -n locales-sv
%{_localedir}/sv_FI*
%{_localedir}/sv_SE*

### sw
%package	sw
Summary:	Base files for localization (Swahili)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	sw
These are the base files for Swahili language localization; you need
it to correctly display 8bits Swahili characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swahili language conventions.

%post		sw
%{loc_add} sw_KE SW_TZ sw_XX

%preun		sw
if [ "$1" = "0" ]; then
	%{loc_del} sw_KE sw_TZ sw_XX
fi

%files		sw
%{_localedir}/sw_KE*
%{_localedir}/sw_TZ*
%{_localedir}/sw_XX*

### ta
%package -n locales-ta
Summary: Base files for localization (Tamil)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
URL: http://www.tamil.net/tscii/

%description -n locales-ta
These are the base files for Tamil language localization; you need
it to correctly display 8bits Tamil characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tamil language conventions.

%post -n locales-ta
%{loc_add} ta_IN ta_LK

%preun -n locales-ta
if [ "$1" = "0" ]; then
	%{loc_del} ta_INta_LK
fi

%files -n locales-ta
%{_localedir}/ta_IN*
%{_localedir}/ta_LK*

### te
%package -n locales-te
Summary: Base files for localization (Telugu)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-te
These are the base files for Telugu language localization; you need
it to correctly display 8bits Telugu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Telugu language conventions.

%post -n locales-te
%{loc_add} te_IN

%preun -n locales-te
if [ "$1" = "0" ]; then
	%{loc_del} te_IN
fi

%files -n locales-te
%{_localedir}/te_IN*

### tg
%package -n locales-tg
Summary: Base files for localization (Tajik)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-tg
These are the base files for Tajik language localization; you need
it to correctly display 8bits Tajik characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tajik language conventions.

%post -n locales-tg
%{loc_add} tg_TJ

%preun -n locales-tg
if [ "$1" = "0" ]; then
	%{loc_del} tg_TJ
fi

%files -n locales-tg
%{_localedir}/tg_TJ*

### th
%package	th
Summary:	Base files for localization (Thai)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	th
These are the base files for Thai language localization; you need
it to correctly display 8bits Thai characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Thai language conventions.

%post		th
%{loc_add} th_TH

%preun		th
if [ "$1" = "0" ]; then
	%{loc_del} th_TH
fi

%files		th
%{_localedir}/th_TH*

### tk
%package -n locales-tk
Summary: Base files for localization (Turkmen)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-tk
These are the base files for Turkmen language localization; you need
it to correctly display 8bits Turkmen characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Turkmen language conventions.

%post -n locales-tk
%{loc_add} tk_TM

%preun -n locales-tk
if [ "$1" = "0" ]; then
	%{loc_del} tk_TM
fi

%files -n locales-tk
%{_localedir}/tk_TM*

### fil
# note: previously named "locales-ph"
%package -n locales-tl
Summary: Base files for localization (Pilipino)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-ph = %{version}-%{release}
Provides: locales-fil = %{version}-%{release}
Obsoletes: locales-ph

%description -n locales-tl
These are the base files for Pilipino (official language of the Philipines)
localization; you need it to correctly display 8bits characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Pilipino language conventions.

%post -n locales-tl
%{loc_add} fil_PH tl_PH

%preun -n locales-tl
if [ "$1" = "0" ]; then
	%{loc_del} fil_PH tl_PH
fi

%files -n locales-tl
%{_localedir}/fil_PH*
%{_localedir}/tl_PH*

### tn
%package -n locales-tn
Summary: Base files for localization (Tswana)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-tn
These are the base files for Tswana language localization; you need
it to correctly display 8bits Tswana characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Tswana language conventions.

%post -n locales-tn
%{loc_add} tn_ZA

%preun -n locales-tn
if [ "$1" = "0" ]; then
	%{loc_del} tn_ZA
fi

%files -n locales-tn
%{_localedir}/tn_ZA*

### tr
# translation from Gorkem Cetin <e077245@narwhal.cc.metu.edu.tr>
%package -n locales-tr
Summary: Base files for localization (Turkish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(tr): Yerelleştirme için temel dosyalar (Türkçe)

%description -n locales-tr
These are the base files for Turkish language localization; you need
it to correctly display 8bits Turkish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Turkish language conventions.

%description -n locales-tr -l tr
Bu dosyalar, Türkçe yerelleştirmesi için gerekli temel bileşenleri içerir.
8bit türkçe karakterleri görmek, Türk diline uygun olarak alfabe, tarih ve
sayı gösterimlerini ve sıralamalarını yapabilmek için bu dosyalara
ihtiyacınız vardır.

%post -n locales-tr
%{loc_add} tr_CY tr_TR

%preun -n locales-tr
if [ "$1" = "0" ]; then
	%{loc_del} tr_CY tr_TR
fi

%files -n locales-tr
%{_localedir}/tr_CY*
%{_localedir}/tr_TR*

### ts
%package -n locales-ts
Summary: Base files for localization (Tsonga)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ts
These are the base files for Tsonga language localization; you need
it to correctly display 8bits Tsonga characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Tsonga language conventions.

%post -n locales-ts
%{loc_add} ts_ZA

%preun -n locales-ts
if [ "$1" = "0" ]; then
	%{loc_del} ts_ZA
fi

%files -n locales-ts
%{_localedir}/ts_ZA*

### tt
%package -n locales-tt
Summary: Base files for localization (Tatar)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-tt
These are the base files for Tatar language localization; you need
it to correctly display 8bits Tatar characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tatar language conventions.

%post -n locales-tt
%{loc_add} tt_RU

%preun -n locales-tt
if [ "$1" = "0" ]; then
	%{loc_del} tt_RU
fi

%files -n locales-tt
%{_localedir}/tt_RU*

### ug
%package -n locales-ug
Summary: Base files for localization (Uyghur)
Group: System/Internationalization
#Icon: bulle-ug.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ug
These are the base files for Uyghur language localization; you need
it to correctly display 8bits Uyghur characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Uyghur language conventions.

%post -n locales-ug
%{loc_add} ug_CN

%preun -n locales-ug
if [ "$1" = "0" ]; then
	%{loc_del} ug_CN
fi

%files -n locales-ug
%{_localedir}/ug_CN*

### unm
%package -n locales-unm
Summary: Base files for localization (Unami)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-unm
These are the base files for Unami language localization; you need
it to correctly display 8bits Unami characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Unami language conventions.

%post -n locales-unm
%{loc_add} unm_US

%preun -n locales-unm
if [ "$1" = "0" ]; then
	%{loc_del} unm_US
fi

%files -n locales-unm
%{_localedir}/unm_US*

### uk
%package -n locales-uk
Summary: Base files for localization (Ukrainian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(ru): Базовые файлы для Украинской локализации
Summary(uk): Базові файли для української локалізації

%description -n locales-uk
These are the base files for Ukrainian language localization; you need
it to correctly display 8bits Ukrainian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Ukrainian language conventions.

%description -n locales-uk -l ru
Базовые файлы для Украинской локализации; нужны для корректного
представления 8-ми битных Украинских символов, а также для правильной
сортировки и представления даты и чисел в соответствии со стандартами
Украинского языка.

%description -n locales-uk -l uk
Базові файли для української локалізації; необхідні для правильного
відображення 8-ми бітних символів українського алфавіту і також для
правильного сортування і подання дати і чисел у відповідності до
стандартів української мови.

%post -n locales-uk
%{loc_add} uk_UA

%preun -n locales-uk
if [ "$1" = "0" ]; then
	%{loc_del} uk_UA
fi

%files -n locales-uk
%{_localedir}/uk_UA*

### ur
%package -n locales-ur
Summary: Base files for localization (Urdu)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ur
These are the base files for Urdu language localization; you need
it to correctly display 8bits Urdu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Urdu language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%post -n locales-ur
%{loc_add} ur_PK

%preun -n locales-ur
if [ "$1" = "0" ]; then
	%{loc_del} ur_PK
fi

%files -n locales-ur
%{_localedir}/ur_PK*

### uz
%package -n locales-uz
Summary: Base files for localization (Uzbek)
Summary(uz): Lokallashtirishning asosiy fayllari (o'zbekcha)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-uz@cyrillic = %{version}-%{release}

%description -n locales-uz
These are the base files for Uzbek language localization; you need
it to correctly display 8bits Uzbek characters, and for proper
alphabetical sorting and representation of dates and numbers
according to Uzbek language conventions.

#%#description -n locales-uz -l uz
#Ushbu asos fayllar Linuxni o'zbekchaga locallashtirish
#uchun qo'llaniladi; siz bularni 8 bit o'zbek
#harflarini to'g'ri ko'rish va tartiblashda qollanasiz.
#O'zbekistonda joriy bo'lgan vaqt, son va valytani
#belgilash qoidalari ham shu fayllarda joylashgan.

%post -n locales-uz
%{loc_add} uz_UZ

%preun -n locales-uz
if [ "$1" = "0" ]; then
	%{loc_del} uz_UZ
fi

%files -n locales-uz
%{_localedir}/uz_UZ*

### ve
%package -n locales-ve
Summary: Base files for localization (Venda)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ve
These are the base files for Venda language localization; you need
it to correctly display 8bits Venda characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Venda language conventions.

%post -n locales-ve
%{loc_add} ve_ZA

%preun -n locales-ve
if [ "$1" = "0" ]; then
	%{loc_del} ve_ZA
fi

%files -n locales-ve
%{_localedir}/ve_ZA*

### vi
# translations by <DaiQuy.nguyen@ulg.ac.be>
%package -n locales-vi
Summary: Base files for localization (Vietnamese)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(vi): Các file cơ sở cho định vị tiếng Việt 

%description -n locales-vi
These are the base files for Vietnamese language localization; you need
it to correctly display 8bits Vietnamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Vietnamese language conventions.

%description -n locales-vi -l vi
Đây là các file cơ sở cho tiếng Việt.
Bạn cần những file này để có thể
biểu diễn chính xác các kí tự tiếng Việt 8 bits,
để sắp xếp và trình bày ngày tháng và số
một cách chính xác theo đúng qui ước ngôn ngữ tiếng Việt.

%post -n locales-vi
%{loc_add} vi_VN

%preun -n locales-vi
if [ "$1" = "0" ]; then
	%{loc_del} vi_VN
fi

%files -n locales-vi
%{_localedir}/vi_VN*

### wa
# translations from Lorint Hendschel <LorintHendschel@skynet.be>
%package -n locales-wa
Summary: Base files for localization (Walloon)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(wa): Maisses fitchîs pol lingaedje walon
Summary(fr): Fichiers de base pour la localisation en langue wallonne

%description -n locales-wa
These are the base files for Walloon language localization; you need
it to correctly display 8bits Walloon characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Walloon language conventions.

%description -n locales-wa -l wa
Vochal les maisses fitchîs pol lingaedje walon. Vos nd avoz dandjî po
hågner les caracteres walons ecôdés so ût bits, po l' arindjmint
alfabetike eyèt po rprezinter les dates eyèt les nombes è walon.

%description -n locales-wa -l fr
Ce paquet contient les définitions de locales en langue walone.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates et des nombres.

%post -n locales-wa
%{loc_add} wa_BE

%preun -n locales-wa
if [ "$1" = "0" ]; then
	%{loc_del} wa_BE
fi

%files -n locales-wa
%{_localedir}/wa_BE*

### wae
%package	wae
Summary:	Base files for localization (Walser)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	wae
These are the base files for Walser language localization; you need
it to correctly display 8bits Walser characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Walser language conventions.

%post		wae
%{loc_add} wae_CH

%preun		wae
if [ "$1" = "0" ]; then
	%{loc_del} wae_CH
fi

%files		wae
%{_localedir}/wae_CH*

### wo
%package -n locales-wo
Summary: Base files for localization (Wolof)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-wo
These are the base files for Wolof language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according
to Wolof language conventions.

%post -n locales-wo
%{loc_add} wo_SN

%preun -n locales-wo
if [ "$1" = "0" ]; then
	%{loc_del} wo_SN
fi

%files -n locales-wo
%{_localedir}/wo_SN

### xh
%package -n locales-xh
Summary: Base files for localization (Xhosa)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-xh
These are the base files for Xhosa language localization; you need
it to correctly display 8bits Xhosa characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%post -n locales-xh
%{loc_add} xh_ZA

%preun -n locales-xh
if [ "$1" = "0" ]; then
	%{loc_del} xh_ZA
fi

%files -n locales-xh
%{_localedir}/xh_ZA*

### yi
%package -n locales-yi
Summary: Base files for localization (Yiddish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
URL: http://www.uyip.org/

%description -n locales-yi
These are the base files for Yiddish language localization; you need
it to correctly display 8bits Yiddish characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Yiddish language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%post -n locales-yi
%{loc_add} yi_US

%preun -n locales-yi
if [ "$1" = "0" ]; then
	%{loc_del} yi_US
fi

%files -n locales-yi
%{_localedir}/yi_US*

### yo
%package -n locales-yo
Summary: Base files for localization (Yoruba)
Group: System/Internationalization
#Icon: bulle-yo.xpm
Requires: locales = %{version}-%{release}

%description -n locales-yo
These are the base files for Yoruba language localization; you need
it to correctly display 8bits Yoruba characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Yoruba language conventions.

%post -n locales-yo
%{loc_add} yo_NG

%preun -n locales-yo
if [ "$1" = "0" ]; then
	%{loc_del} yo_NG
fi

%files -n locales-yo
%{_localedir}/yo_NG*

### yue
%package	yue
Summary:	Base files for localization (Yue Chinese (Cantonese))
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description	yue
These are the base files for Yue Chinese (Cantonese) language localization;
you need it to correctly display 8bits Walser characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Yue Chinese (Cantonese) language conventions.

%post		yue
%{loc_add} yue_HK

%preun		yue
if [ "$1" = "0" ]; then
	%{loc_del} yue_HK
fi

%files		yue
%{_localedir}/yue_HK*

### zh
# translation (zh_TW) from <informer@linux1.cgu.edu.tw>
# zh_CN converted from zh_TW.Big5 with b5togb; corrections welcome.
%package -n locales-zh
Summary: Base files for localization (Chinese)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-zh_CN = %{version}-%{release}
Provides: locales-zh_TW = %{version}-%{release}
Provides: locales-zh_SG = %{version}-%{release}
Provides: locales-zh_HK = %{version}-%{release}
Obsoletes: libwcsmbs wcsmbs-locale
Summary(zh_CN): 中文地方化的基本档案
Summary(zh_TW): 中文地方化的基本檔案

%description -n locales-zh
These are the base files for Chinese language localization; you need
it to correctly display 8bits and 7bits chinese codes, and for proper
representation of dates and numbers according to chinese language conventions.
Set the LANG variable to "zh_CN" to use simplified chinese (GuoBiao encoding)
or to "zh_TW.Big5" to use traditional characters (Big5 encoding)

%description -n locales-zh -l zh_CN
本档包含了中文地方化(localization)的基本档案; 你需要这些档案才能正确的
显示中文的日期。将环境变数 "LANG" 设定为 "zh_CN" 可以显示简体中文(国标
码),设定为 "zh_TW" 则可显示繁体中文(大五码)。 
%description -n locales-zh -l zh_TW
本檔包含了中文地方化(localization)的基本檔案; 你需要這些檔案才能正確的
顯示中文的日期。將環境變數 "LANG" 設定為 "zh_CN" 可以顯示簡體中文(國標
碼),設定為 "zh_TW" 則可顯示繁體中文(大五碼)。 

%post -n locales-zh
%{loc_add} nan_TW@latin zh_CN zh_HK zh_SG zh_TW

%preun -n locales-zh
if [ "$1" = "0" ]; then
	%{loc_del} nan_TW@latin zh_CN zh_HK zh_SG zh_TW
fi

%files -n locales-zh
%{_localedir}/nan_TW@latin
%{_localedir}/zh_CN*
%{_localedir}/zh_HK*
%{_localedir}/zh_SG*
%{_localedir}/zh_TW*

### zu
%package -n locales-zu
Summary: Base files for localization (Zulu)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-zu
These are the base files for Zulu language localization; you need
it to correctly display 8bits Zulu characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%post -n locales-zu
%{loc_add} zu_ZA

%preun -n locales-zu
if [ "$1" = "0" ]; then
	%{loc_del} zu_ZA
fi

%files -n locales-zu
%{_localedir}/zu_ZA*

%prep
%setup -qcT

cp %{SOURCE0} %{SOURCE1} .
for i in `grep '^#LIST_LOCALES=' iso14651_hack | cut -d= -f2 | tr ':' ' '`
do
	cat iso14651_hack | sed "s/#hack-$i#//" > iso14651_$i
done

# for turkic languages (upperwasing/lowercasing of iwithdot/dotlessi)
cat /usr/share/i18n/locales/i18n | \
	sed 's/<U0069>,<U0049>/<U0069>,<U0130>/' | \
	sed 's/<U0049>,<U0069>/<U0049>,<U0131>/' > i18n_tr

		
# copy various unhabitual charsets and other stuff
for DEF_CHARSET in \
	es@tradicional
do
	cp %{_sourcedir}/$DEF_CHARSET .
done

# special handling for PRC
%if %build_for_PRC
	cp %{_sourcedir}/zh_TW_2 zh_TW
%endif

# copy local locales unavailable in glibc
for loc in eo_XX es@tradicional nds_DE@traditional sw_XX
do
	cp %{_sourcedir}/$loc .
done

# copy modified glibc locales
for loc in ar_SA az_AZ bs_BA dz_BT es_ES es_US es_CO km_KH ku_TR ky_KG sq_AL \
           tg_TJ tr_TR vi_VN wa_BE yi_US zh_CN
do
	cp %{_sourcedir}/$loc .
done

%build
LOCALEDIR=root%{_localedir}
install -d $LOCALEDIR

# making default charset pseudo-locales
# those will be symlinked (for LC_CTYPE, LC_COLLATE mainly) from
# a lot of other locales, thus saving space
for DEF_CHARSET in UTF-8 ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 \
	 ISO-8859-5 ISO-8859-7 ISO-8859-9 \
	 ISO-8859-13 ISO-8859-14 ISO-8859-15 KOI8-R KOI8-U CP1251 
do
	# find the charset definition
    if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET ]; then
    	if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET.gz ]; then
			cp %{_sourcedir}/$DEF_CHARSET .
			DEF_CHARSET=%{_sourcedir}/$DEF_CHARSET
		fi
	fi
	# don't use en_DK because of LC_MONETARY
	localedef -c -f $DEF_CHARSET -i en_US $LOCALEDIR/`basename $DEF_CHARSET` || :
done

# fix for Arabic yes/no expr
for i in /usr/share/i18n/locales/ar_??
do
	if [ ! -r "%{_sourcedir}/`basename $i`" ]; then
		cat $i | \
		sed 's/^\(yesexpr.*\)<U0646>/\1<U0646><U0079><U0059>/' | \
		sed 's/^\(noexpr.*\)<U0644>/\1<U0644><U006E><U004E>/' > \
		./`basename $i`
	fi
done

# fix for locales using monday as first week day
# http://sources.redhat.com/bugzilla/show_bug.cgi?id=3035
for i in /usr/share/i18n/locales/be_BY /usr/share/i18n/locales/cy_GB \
	/usr/share/i18n/locales/de_?? /usr/share/i18n/locales/el_GR \
	/usr/share/i18n/locales/es_CL \
	/usr/share/i18n/locales/es_MX /usr/share/i18n/locales/fr_?? \
	/usr/share/i18n/locales/fy_NL /usr/share/i18n/locales/it_?? \
	/usr/share/i18n/locales/lt_LT /usr/share/i18n/locales/mi_NZ \
	/usr/share/i18n/locales/nl_BE /usr/share/i18n/locales/nl_NL \
	/usr/share/i18n/locales/pt_PT /usr/share/i18n/locales/ru_UA \
	/usr/share/i18n/locales/se_NO /usr/share/i18n/locales/sv_FI \
	/usr/share/i18n/locales/*_ES vi_VN
do
	LOCALENAME=`basename $i`
	if [ -r %{_sourcedir}/$i ]; then
		DEF_LOCALE_FILE="%{_sourcedir}/$i"
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/$LOCALENAME"
	fi
	if ! grep '^week\>' $DEF_LOCALE_FILE > /dev/null && \
	   ! grep '^first_weekday\>' $DEF_LOCALE_FILE > /dev/null && \
	   ! grep '^first_workday\>' $DEF_LOCALE_FILE > /dev/null
	then
		cat $DEF_LOCALE_FILE | sed \
			's/\(END LC_TIME\)/week 7;19971201;4\nfirst_weekday 1\nfirst_workday 1\n\1/' > \
		./$LOCALENAME
	fi
done

%make DESTDIR=root

localedef -c -f ISO-8859-15 -i nds_DE@traditional $LOCALEDIR/nds_DE@traditional
localedef -c -f ISO-8859-1  -i nds_DE@traditional $LOCALEDIR/nds_DE@traditional.ISO-8859-1
localedef -c -f UTF-8       -i nds_DE@traditional $LOCALEDIR/nds_DE@traditional.UTF-8
localedef -c -f UTF-8       -i sw_XX              $LOCALEDIR/sw_XX
localedef -c -f UTF-8       -i eo_XX              $LOCALEDIR/eo_XX
localedef -c -f UTF-8       -i wal_ET             $LOCALEDIR/wal_ET || :

# create the default locales for languages whith multiple locales
localedef -c -f ISO-8859-15 -i ./es@tradicional $LOCALEDIR/es@tradicional

#=========================================================
#
# special non-UTF-8 locales for compatibility
#

# Esperanto
localedef -c -f ISO-8859-3 -i eo_XX $LOCALEDIR/eo_XX.ISO-8859-3

# en_BE is required for conformance to LI18NUX2000/OpenI18N
# (http://www.openi18n.org/docs/pdf/OpenI18N1.3.pdf)
for i in $LOCALEDIR/en_IE* ; do
	mkdir $LOCALEDIR/en_BE`basename $i | cut -b6- `
	cp -var $i/* $LOCALEDIR/en_BE`basename $i | cut -b6- `
	for j in LC_MONETARY LC_TELEPHONE LC_ADDRESS
	do
		cp -var $LOCALEDIR/nl_BE`basename $i | cut -b6- `/$j \
			$LOCALEDIR/en_BE`basename $i | cut -b6- `
	done
done

#=========================================================
# XXX: duplicate of nb_NO (remove from glibc?)
rm -rf $LOCALEDIR/no_NO*

%install
install -m755 %{SOURCE2} -D %{buildroot}%{loc_add}
install -m755 %{SOURCE3} -D %{buildroot}%{loc_del}

install -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/locales

cp -a root/* %{buildroot}

perl %{SOURCE5} %{buildroot}%{_localedir}

pushd %{buildroot}%{_localedir}
for i in `echo ??_??* ???_??*`; do
	LC_ALL=C perl %{SOURCE6} $i
done
popd
