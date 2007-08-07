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
%define glibc_ver 2.6.1
%define glibc_epoch 6
%define version   %{glibc_ver}
%define release   %mkrel 1
# FIXME: please check on next build those we really need
%define _unpackaged_files_terminate_build 1

# to define when building for PRC
#%define build_for_PRC 1

# shorthands for the post scripts
%define loc_add /usr/bin/locale_install.sh
%define loc_del /usr/bin/locale_uninstall.sh

Summary: Base files for localization
Name: locales
Version: %{version}
Release: %{release}
License: GPL
Group: System/Internationalization

# updated to include unicode 5.0 introduced latin/cyrullic/greek letters
#
Source1: iso14651_hack
# scripts to install/uninstall a locale
Source2: locale_install.sh
Source3: locale_uninstall.sh
# the default "i18n" locale; updated to unicode 5.0
Source4: i18n
# the UTF-8 charset definition; updated to unicode 5.0
Source5: UTF-8.gz

# this one is on glibc, however there is the politic issue
# of the naming of Taiwan 
Source6: zh_TW_2

# locales data
Source16: sw_XX
Source17: ku_TR
Source18: eo_XX
Source19: ky_KG
Source20: iu_CA
Source21: fur_IT
Source22: km_KH
Source23: fil_PH
Source24: nds_DE
Source25: nds_DE@traditional
Source26: nds_NL
Source27: pap_AN
Source29: sc_IT
Source30: li_NL
Source31: li_BE
Source32: tk_TM
Source33: fy_DE
Source34: fy_NL
Source35: ik_CA
Source36: ber_MA
Source37: ber_DZ
Source38: dz_BT
# provisional Uyghur locale
Source39: ug_CN
# provisional locales for Nigeria
Source40: en_NG
Source41: ha_NG
Source42: ig_NG
Source43: yo_NG
# glibc no longer comes with Latn version...
Source44: http://srpski.org/locale/sr_CS@Latn

# Those exist in glibc >= 2.3.2 but the attached ones
# are more correct/more complete

# patched for the euro
Source49: sl_SI
# all ar_?? locales in glibc 2.3.5 are missing "Yy" and "Nn" in 
# version in glibc 2.3.5 has wrong yexexpr/noexpr and wrong LC_COLLATE
Source50: ar_SA
# corrected month names
Source51: az_AZ
# LC_COLLATE has one line wrong
Source52: bs_BA
# rewritten to take profit of new glibc reordering possibilities
Source53: es_ES
Source54: es_US
Source55: es@tradicional
# Colombia uses "Letter" paper size
Source56: es_CO
# corrected LC_COLLATE
Source58: sq_AL
# ours has yesexpr using tajik
Source59: tg_TJ
# changed LC_COLLATE to new format
Source60: tr_TR_collate
# tr_TR thet includes "i18n_tr" (generated with a simple regexp replacing)
Source61: tr_TR
# LC_COLLATE for vietnamese is incorrect in glibc, and LC_CTIME seems
# wrong too... 
Source63: vi_VN
# fixes in weekday names
Source64: wa_BE
# various spelling fixes
Source65: yi_US
# changed date format strings
Source66: zh_CN

# ethiopic locales (violate ISO-639! not packaged)
Source67: ad_ET
Source68: qo_ET
Source69: sx_ET
Source70: sz_ET

# it is arch dependent in fact
#BuildArchitectures: noarch
# to build this package glibc = %{glibc_ver} is needed (for locales definitions)
Prereq: glibc = %{glibc_epoch}:%{glibc_ver}
# no need to check for dependencies when building, there is no executables here
AutoReqProv: no
BuildRoot: %{_tmppath}/locales-root
# locales are very dependent on glibc version
Requires: glibc = %{glibc_epoch}:%{glibc_ver}
# post scripts use grep, perl, etc.
Requires(post): perl-base rpm coreutils
Requires(postun): perl-base rpm coreutils
# glibc >= 2.2.5-6mdk now comes with glibc-i18ndata package
BuildRequires: glibc-i18ndata = %{glibc_epoch}:%{glibc_ver}
# needed for dz_BT (LC_COLLATE with more than 250 rules)
BuildRequires: glibc >= 2.3.6-2mdk

%description
These are the base files for language localization.
You also need to install the specific locales-?? for the
language(s) you want. Then the user need to set the
LANG variable to their preferred language in their
~/.profile configuration file.

%prep

%build
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin/
install -m 755 %{SOURCE2} ${RPM_BUILD_ROOT}%{loc_add}
install -m 755 %{SOURCE3} ${RPM_BUILD_ROOT}%{loc_del}

#mv /usr/share/locale /usr/share/locale_bak
mkdir -p $RPM_BUILD_ROOT/usr/share/locale
LOCALEDIR=$RPM_BUILD_ROOT/usr/share/locale

rm -rf locales-%{version}
mkdir -p locales-%{version} ; cd locales-%{version}

cp $RPM_SOURCE_DIR/iso14651_hack iso14651_t1
cp $RPM_SOURCE_DIR/iso14651_hack .
for i in `grep '^#LIST_LOCALES=' iso14651_hack | cut -d= -f2 | tr ':' ' '`
do
	cat iso14651_hack | sed "s/#hack-$i#//" > iso14651_$i
done

# copy updated UTF-8/i18n files (we check for U0513 introduced in unicode 5.0)
if ! zgrep 'U0513' /usr/share/i18n/charmaps/UTF-8.gz >& /dev/null
then
 [ -r $RPM_SOURCE_DIR/UTF-8.gz ] && zcat $RPM_SOURCE_DIR/UTF-8.gz > UTF-8
else
 echo "the glibc UTF-8 file is already unicode 5.0 or higher"
fi
if ! grep 'U0513' /usr/share/i18n/locales/i18n >& /dev/null
then
 [ -r $RPM_SOURCE_DIR/i18n ] && cp $RPM_SOURCE_DIR/i18n i18n
else
 cp /usr/share/i18n/locales/i18n i18n
fi

# for turkic languages (upperwasing/lowercasing of iwithdot/dotlessi)
cat i18n | \
	sed 's/<U0069>,<U0049>/<U0069>,<U0130>/' | \
	sed 's/<U0049>,<U0069>/<U0049>,<U0131>/' > i18n_tr

		
# copy various unhabitual charsets and other stuff
# en_NG is needed for proper building of other *_NG locales
for DEF_CHARSET in \
	es@tradicional en_NG
do
	cp $RPM_SOURCE_DIR/$DEF_CHARSET .
done

# special handling for PRC
%if %build_for_PRC
	cp $RPM_SOURCE_DIR/zh_TW_2 zh_TW
%endif

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
			cp $RPM_SOURCE_DIR/$DEF_CHARSET .
			DEF_CHARSET=$RPM_SOURCE_DIR/$DEF_CHARSET
		fi
	fi
	# don't use en_DK because of LC_MONETARY
	localedef -c -f $DEF_CHARSET -i en_US $LOCALEDIR/`basename $DEF_CHARSET` || :
done

# fix for Arabic yes/no expr
for i in /usr/share/i18n/locales/ar_??
do
	if [ ! -r "$RPM_SOURCE_DIR/`basename $i`" ]; then
		cat $i | \
		sed 's/^\(yesexpr.*\)<U0646>/\1<U0646><U0079><U0059>/' | \
		sed 's/^\(noexpr.*\)<U0644>/\1<U0644><U006E><U004E>/' > \
		./`basename $i`
	fi
done
# fix for locales using monday as first week day
# http://sources.redhat.com/bugzilla/show_bug.cgi?id=3035
for i in az_AZ be_BY bg_BG bs_BA cs_CZ cy_GB da_DK et_EE fi_FI \
	lt_LT mi_NZ pl_PL pt_PT ro_RO sk_SK sr_CS uk_UA vi_VN zh_CN \
	/usr/share/i18n/locales/de_?? /usr/share/i18n/locales/es_?? \
	/usr/share/i18n/locales/el_?? /usr/share/i18n/locales/fr_?? \
	/usr/share/i18n/locales/it_?? /usr/share/i18n/locales/ru_?? \
	/usr/share/i18n/locales/sv_?? /usr/share/i18n/locales/tr_?? \
	/usr/share/i18n/locales/*_BE /usr/share/i18n/locales/*_NL \
	/usr/share/i18n/locales/*_CH /usr/share/i18n/locales/*_ES \
	/usr/share/i18n/locales/*_NO
do
	LOCALENAME=`basename $i`
	if [ -r $RPM_SOURCE_DIR/$i ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/$i"
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/$LOCALENAME"
	fi
	if ! grep '^week\>' $DEF_LOCALE_FILE > /dev/null ; then
		cat $DEF_LOCALE_FILE | sed 's/\(END LC_TIME\)/week 7;19971201;4\n\1/' > \
		./$LOCALENAME
	fi
done



# languages which have only one locale; use the language name as locale
# name for them; that makes the localization far easier
#
# Not yet build, to add later: pap_AN
# uz_UZ is purposedly excluded (handled separately),
# as we default to cyrillic now
#
for i in \
	 af_ZA am_ET an_ES as_IN az_AZ be_BY bg_BG \
	 br_FR bs_BA byn_ER cs_CZ cy_GB da_DK dz_BT \
	 eo_XX et_EE eu_ES fa_IR fi_FI \
	 fo_FO fur_IT fy_DE fy_NL ga_IE gd_GB gl_ES gu_IN gv_GB \
	 ha_NG he_IL hi_IN hr_HR hsb_DE hu_HU hy_AM \
	 id_ID ig_NG ik_CA is_IS iu_CA ja_JP \
	 ka_GE kk_KZ kl_GL km_KH kn_IN ko_KR ku_TR kw_GB ky_KG \
	 lg_UG lo_LA lt_LT lv_LV mg_MG mi_NZ mk_MK ml_IN mn_MN mr_IN ms_MY \
	 mt_MT nb_NO ne_NP nn_NO nr_ZA nso_ZA oc_FR om_ET om_KE \
	 fil_PH pl_PL ro_RO rw_RW sc_IT se_NO si_LK sid_ET sk_SK sl_SI \
	 sq_AL sr_CS ss_ZA st_ZA ta_IN te_IN tg_TJ th_TH ti_ER ti_ET \
	 tig_ER tk_TM tl_PH tn_ZA ts_ZA tt_RU ug_CN uk_UA ur_PK \
	 ve_ZA vi_VN wa_BE wal_ET xh_ZA \
	 yi_US yo_NG zh_CN zh_HK zh_SG zh_TW zu_ZA
do
	LOCALENAME=$i
	if [ -r ./$i ]; then
		DEF_LOCALE_FILE="./$i"
	elif [ -r $RPM_SOURCE_DIR/$i ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/$i"
		cp $RPM_SOURCE_DIR/$i .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/$i"
	fi
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "$i" in
		af_*) DEF_CHARSET="ISO-8859-1" ;;
		bs_*|cs_*|hr_*|hu_*|pl_*|ro_*|sk_*|sl_*) DEF_CHARSET="ISO-8859-2" ;;
		lt_*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		br_*|da_*|et_*|eu_*) DEF_CHARSET="ISO-8859-15";;
		fi_*|fo_*|fur_*|ga_*|gl_*|is_*) DEF_CHARSET="ISO-8859-15";;
		nn_*|no_*|nb_*|oc_*|sc_*|sq_*|wa_*) DEF_CHARSET="ISO-8859-15";;
		be_*|bg_*) DEF_CHARSET="CP1251" ;;
		ru_*) DEF_CHARSET="KOI8-R" ;;
		uk_*) DEF_CHARSET="KOI8-U" ;;
		ja_*) DEF_CHARSET="EUC-JP" ;;
		ko_*) DEF_CHARSET="EUC-KR" ;;
		th_*) DEF_CHARSET="TIS-620" ;;
		zh_CN|zh_SG) DEF_CHARSET="GB2312" ;;
		zh_TW|zh_TW) DEF_CHARSET="BIG5" ;;
	esac
	DEF_LOCALE=`basename $i`
    case "$DEF_LOCALE" in
		*@*) VARIANT="`echo $DEF_LOCALE | sed 's/^[^@]*@/@/'`" ;
		     DEF_LOCALE="`echo $DEF_LOCALE | sed s/${VARIANT}//`" ;;
	    *) VARIANT="" ;;
    esac
	DEF_LANG=`echo $DEF_LOCALE | cut -d'_' -f1`
	# find the charset definition
    if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET ]; then
    	if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET.gz ]; then
			cp $RPM_SOURCE_DIR/$DEF_CHARSET .
			DEF_CHARSET=$RPM_SOURCE_DIR/$DEF_CHARSET
		fi
	fi
	# if some locale returns a non 0 return code it isn't important
	[ "$DEF_LANG" != "${LOCALENAME}" -a ! -r "$LOCALEDIR/$DEF_LANG" ] && \
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LANG${VARIANT}  || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}${VARIANT} || :
	[ "$DEF_CHARSET" != "BIG5" -a "$DEF_CHARSET" != "UTF-8" ] && \
	(localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.`basename ${DEF_CHARSET}`${VARIANT} || : )
	localedef -c -f UTF-8 -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.UTF-8${VARIANT} || :
done

# languages which have several locales
#
# en_NG not yet on glibc
#
for i in $RPM_SOURCE_DIR/nds_??* $RPM_SOURCE_DIR/li_?? \
	 $RPM_SOURCE_DIR/fy_??   $RPM_SOURCE_DIR/sw_?? \
	 /usr/share/i18n/locales/aa_??* /usr/share/i18n/locales/ar_?? \
	 $RPM_SOURCE_DIR/ber_?? \
	 /usr/share/i18n/locales/bn_?? /usr/share/i18n/locales/ca_?? \
	 /usr/share/i18n/locales/de_?? /usr/share/i18n/locales/el_?? \
	 $RPM_SOURCE_DIR/en_NG \
	 /usr/share/i18n/locales/en_?? /usr/share/i18n/locales/es_?? \
	 /usr/share/i18n/locales/fr_?? /usr/share/i18n/locales/gez_??* \
	 /usr/share/i18n/locales/it_?? /usr/share/i18n/locales/nl_?? \
	 /usr/share/i18n/locales/pa_?? /usr/share/i18n/locales/pt_?? \
	 /usr/share/i18n/locales/ru_?? \
	 /usr/share/i18n/locales/so_?? /usr/share/i18n/locales/sv_?? \
	 /usr/share/i18n/locales/tr_??
do
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "`basename $i`" in
		en_IN|en_NG) DEF_CHARSET="UTF-8" ;;
		en_IE|es_ES) DEF_CHARSET="ISO-8859-15" ;;
		en_*|es_*) DEF_CHARSET="ISO-8859-1" ;;
		bs_*|cs_*|hr_*|hu_*|pl_*|ro_*|sk_*|sl_*) DEF_CHARSET="ISO-8859-2" ;;
		el_*) DEF_CHARSET="ISO-8859-7" ;;
		tr_*) DEF_CHARSET="ISO-8859-9" ;;
		lt_*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		ca_*|de_*|fr_*|it_*|nl_*|pt_*|sv_*) DEF_CHARSET="ISO-8859-15";;
		fy_*|nds_*|li_*) DEF_CHARSET="ISO-8859-15";;
		ru_*) DEF_CHARSET="KOI8-R" ;;
	esac
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
	elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
		cp /usr/share/i18n/locales/`basename $i` .
	fi
	DEF_LOCALE=`basename $i`
    case "$DEF_LOCALE" in
		*@*) VARIANT="`echo $DEF_LOCALE | sed 's/^[^@]*@/@/'`" ;
		     DEF_LOCALE="`echo $DEF_LOCALE | sed s/${VARIANT}//`" ;;
	    *) VARIANT="" ;;
    esac
	# if some locale returns a non 0 return code it isn't important
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE${VARIANT} || :
	# for compatibility 
	[ "$DEF_CHARSET" = "ISO-8859-15" ] && \
	(localedef -c -f ISO-8859-1 -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.ISO-8859-1${VARIANT} || : )
	[ "$DEF_CHARSET" != "UTF-8" ] && \
	(localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.`basename ${DEF_CHARSET}`${VARIANT} || : )
	localedef -c -f UTF-8 -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.UTF-8${VARIANT} || :
done

# locales using ISO-8859-15 that are not for the default locale of their
# respectives languages
for i in de_AT de_BE de_LU en_IE fi_FI fr_BE fr_LU nl_BE sv_FI
do
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
    elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
    else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
    fi
	DEF_LANG=`basename $i | cut -d'_' -f1 `
	DEF_LOCALE=`basename $i`
	DEF_CHARSET=ISO-8859-15
	
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE || :
	# for compatibility 
	localedef -c -f ISO-8859-1 -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-1 || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-15 || :
done

# locales using iso-8859-15 which are the default ones for their respective
# languages
for i in br_FR ca_ES da_DK de_DE es_ES eu_ES fi_FI fr_FR ga_IE \
	 gl_ES is_IS it_IT li_NL nds_DE nl_NL pt_PT wa_BE
do
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
    elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
	fi
	DEF_LANG=`basename $i | cut -d'_' -f1 `
	DEF_LOCALE=`basename $i`
	DEF_CHARSET=ISO-8859-15
		
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LANG || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE || :
	# for compatibility 
	localedef -c -f ISO-8859-1   -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-1 || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-15 || :
done

# create the default locales for languages whith multiple locales
localedef -c -f UTF-8       -i ar_EG $LOCALEDIR/ar || :
localedef -c -f ISO-8859-7  -i el_GR $LOCALEDIR/el
localedef -c -f ISO-8859-1  -i en_US $LOCALEDIR/en
localedef -c -f UTF-8       -i pa_IN $LOCALEDIR/pa
localedef -c -f KOI8-R      -i ru_RU $LOCALEDIR/ru
localedef -c -f ISO-8859-15 -i sv_SE $LOCALEDIR/sv
localedef -c -f ISO-8859-9  -i tr_TR $LOCALEDIR/tr
#localedef -c -f ISO-8859-1  -i $RPM_SOURCE_DIR/nds_DE $LOCALEDIR/nds || :
localedef -c -f ISO-8859-15 -i ./es@tradicional $LOCALEDIR/es@tradicional || :

#=========================================================
#
# special non-UTF-8 locales for compatibility
#

# Bielorussian
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be || :
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be_BY || :
localedef -c -f ISO-8859-5 -i be_BY $LOCALEDIR/be_BY.ISO-8859-5 || :

# Esperanto
localedef -c -f ISO-8859-3 -i eo_XX $LOCALEDIR/eo_XX.ISO-8859-3 || :

# estonian can use iso-8859-15 and iso-8859-4
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et || :
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et_EE || :
localedef -c -f ISO-8859-4  -i et_EE $LOCALEDIR/et_EE.ISO-8859-4 || :
localedef -c -f ISO-8859-13 -i et_EE $LOCALEDIR/et_EE.ISO-8859-13 || :

# Finnish default must be iso8859-15
localedef -c -f ISO-8859-1  -i fi_FI $LOCALEDIR/fi_FI.ISO-8859-1 || :

# Hebrew -- for old compatibility and for use with Wine
localedef -c -f ISO-8859-8 -i he_IL $LOCALEDIR/he_IL.ISO-8859-8 || :
localedef -c -f CP1255     -i he_IL $LOCALEDIR/he_IL.CP1255 || :

# Armenian -- for old compatibility
localedef -c -f ARMSCII-8 -i hy_AM $LOCALEDIR/hy_AM.ARMSCII-8 || :

# georgian -- for old compatibility
localedef -c -f GEORGIAN-ACADEMY -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-ACADEMY || :
localedef -c -f GEORGIAN-PS      -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-PS || :

# Kurdish 
localedef -c -f ISO-8859-9 -i ku_TR $LOCALEDIR/ku_TR.ISO-8859-9 || :

# Lithuanian
localedef -c -f ISO-8859-13 -i lt_LT $LOCALEDIR/lt || :
localedef -c -f ISO-8859-13 -i lt_LT $LOCALEDIR/lt_LT || :
localedef -c -f ISO-8859-4  -i lt_LT $LOCALEDIR/lt_LT.ISO-8859-4 || :
localedef -c -f ISO-8859-4  -i lt_LT $LOCALEDIR/lt_LT.ISO-8859-13 || :

# Latvian
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv || :
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv_LV || :
localedef -c -f ISO-8859-4  -i lv_LV $LOCALEDIR/lv_LV.ISO-8859-4 || :
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv_LV.ISO-8859-13 || :

# Maltese -- for old compatibility
localedef -c -f ISO-8859-3 -i mt_MT $LOCALEDIR/mt_MT.ISO-8859-3 || :

# Norwegian bokmål -- for old compatibility
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no || :
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no_NO || :
localedef -c -f ISO-8859-1  -i nb_NO $LOCALEDIR/no_NO.ISO-8859-1 || :
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no_NO.ISO-8859-15 || :
localedef -c -f UTF-8       -i nb_NO $LOCALEDIR/no_NO.UTF-8 || : 

# special case for romanian
localedef -c -f ISO-8859-2  -i ./ro_RO $LOCALEDIR/ro_RO.ISO-8859-2
localedef -c -f ISO-8859-16 -i ./ro_RO $LOCALEDIR/ro_RO.ISO-8859-16
localedef -c -f UTF-8 -i       ./ro_RO $LOCALEDIR/ro_RO.UTF-8
# default, using latin2 for compatibility
localedef -c -f ISO-8859-2 -i  ./ro_RO $LOCALEDIR/ro_RO
localedef -c -f ISO-8859-2 -i  ./ro_RO $LOCALEDIR/ro

# Russian uses koi8-r by default, iso-8859-5 is a second choice
# "ru_RU" locale set to ISO-8859-5 for compatibility reasons
localedef -c -f KOI8-R     -i ru_RU $LOCALEDIR/ru_RU || :
localedef -c -f KOI8-R     -i ru_RU $LOCALEDIR/ru_RU.KOI8-R || :
localedef -c -f ISO-8859-5 -i ru_RU $LOCALEDIR/ru_RU.ISO-8859-5 || :
localedef -c -f CP1251     -i ru_RU $LOCALEDIR/ru_RU.CP1251 || :
# Russian in Ukrainia can use koi8-u
localedef -c -f KOI8-R     -i ru_UA $LOCALEDIR/ru_UA.KOI8-R || :
localedef -c -f KOI8-U     -i ru_UA $LOCALEDIR/ru_UA.KOI8-U || :
localedef -c -f ISO-8859-5 -i ru_UA $LOCALEDIR/ru_UA.ISO-8859-5 || :
localedef -c -f CP1251     -i ru_UA $LOCALEDIR/ru_UA.CP1251 || :

# Albanian
localedef -c -f ISO-8859-1 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-1 || :
localedef -c -f ISO-8859-2 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-2 || :

# Serbian
localedef -c -f ISO-8859-5  -i sr_CS $LOCALEDIR/sr_CS.ISO-8859-5 || :
localedef -c -f CP1252      -i sr_CS $LOCALEDIR/sr_CS.CP1251 || :
cp $RPM_SOURCE_DIR/sr_CS@Latn .
if [ -r "sr_CS@Latn" ]; then
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr@Latn || :
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr_CS@Latn || :
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr_CS.UTF-8@Latn || :
localedef -c -f ISO-8859-2 -i ./sr_CS@Latn $LOCALEDIR/sr_CS.ISO-8859-2@Latn || :
fi
# for old compatibility
if [ -r "sr_CS" ]; then
localedef -c -f UTF-8      -i ./sr_CS $LOCALEDIR/sr_YU || :
localedef -c -f ISO-8859-5 -i ./sr_CS $LOCALEDIR/sr_YU.ISO-8859-5 || :
localedef -c -f CP1251     -i ./sr_CS $LOCALEDIR/sr_YU.CP1251 || :
localedef -c -f UTF-8      -i ./sr_CS $LOCALEDIR/sr_YU.UTF-8 || :
fi
if [ -r "sr_CS@Latn" ]; then
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sr_YU@Latn || :
localedef -c -f ISO-8859-2 -i ./sr_CS@Latn $LOCALEDIR/sr_YU.ISO-8859-2@Latn ||:
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sr_YU.UTF-8@Latn || :
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sh_YU || :
localedef -c -f ISO-8859-2 -i ./sr_CS@Latn $LOCALEDIR/sh_YU.ISO-8859-2 || :
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sh_YU.UTF-8 || :
fi

# Turkmen
localedef -c -f ISO-8859-2 -i tk_TM $LOCALEDIR/tk_TM.ISO-8859-2 || :

# Provide cp1251 for Ukrainian too...
localedef -c -f CP1251     -i uk_UA $LOCALEDIR/uk_UA.CP1251 || :

# Uzbek
[ -r /usr/share/i18n/locales/uz_UZ ] && \
	cp /usr/share/i18n/locales/uz_UZ uz_UZ@Latn
[ -r /usr/share/i18n/locales/uz_UZ@Latn ] && \
	cp -f /usr/share/i18n/locales/uz_UZ@Latn uz_UZ@Latn
if [ -r "uz_UZ@Latn" ]; then
localedef -c -f ISO-8859-1  -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.ISO-8859-1 || :
localedef -c -f ISO-8859-9  -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.ISO-8859-9 || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz@Latn || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ@Latn || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.UTF-8@Latn || :
fi
[ -r /usr/share/i18n/locales/uz_UZ@cyrillic ] && \
	cp /usr/share/i18n/locales/uz_UZ@cyrillic uz_UZ@Cyrl
[ -r /usr/share/i18n/locales/uz_UZ@Cyrl ] && \
	cp /usr/share/i18n/locales/uz_UZ@Cyrl uz_UZ@Cyrl
if [ -r "uz_UZ@Cyrl" ]; then
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ.UTF-8 || :
# for compatibility
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ.UTF-8@Cyrl || :
fi

# Vietnamese -- for old compatibility
localedef -c -f VISCII     -i vi_VN $LOCALEDIR/vi_VN.VISCII || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN-5712 || :

# en_BE is required for conformance to LI18NUX2000
for i in $LOCALEDIR/en_IE* ; do
	mkdir $LOCALEDIR/en_BE`basename $i | cut -b6- `
	cp -var $i/* $LOCALEDIR/en_BE`basename $i | cut -b6- `
	for j in LC_MONETARY LC_TELEPHONE LC_ADDRESS
	do
		cp -var $LOCALEDIR/nl_BE`basename $i | cut -b6- `/$j \
			$LOCALEDIR/en_BE`basename $i | cut -b6- `
	done
done

# celtic languages may want to use iso-8859-14
localedef -c -f ISO-8859-14 -i br_FR $LOCALEDIR/br_FR.ISO-8859-14 || :
localedef -c -f ISO-8859-14 -i cy_GB $LOCALEDIR/cy_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-14 -i ga_IE $LOCALEDIR/ga_IE.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i gd_GB $LOCALEDIR/gd_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i gd_GB $LOCALEDIR/gd_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i gv_GB $LOCALEDIR/gv_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i gv_GB $LOCALEDIR/gv_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i kw_GB $LOCALEDIR/kw_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i kw_GB $LOCALEDIR/kw_GB.ISO-8859-14 || :

# Chinese
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh || :
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh_CN || :
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh_CN.GB2312 || :
localedef -c -f GBK       -i zh_CN $LOCALEDIR/zh_CN.GBK || :
localedef -c -f GB18030   -i zh_CN $LOCALEDIR/zh_CN.GB18030 || :
localedef -c -f UTF-8     -i zh_CN $LOCALEDIR/zh_CN.UTF-8 || :
localedef -c -f BIG5HKSCS -i zh_HK $LOCALEDIR/zh_HK || :
localedef -c -f GB18030   -i zh_HK $LOCALEDIR/zh_HK.GB18030 || :
localedef -c -f BIG5      -i zh_TW $LOCALEDIR/zh_TW || :
localedef -c -f BIG5      -i zh_TW $LOCALEDIR/zh_TW.Big5 || :

# Filipino -- for old compatibility (to remove in the future)
localedef -c -f UTF-8       -i fil_PH $LOCALEDIR/ph || :
localedef -c -f UTF-8       -i fil_PH $LOCALEDIR/ph_PH || : 
localedef -c -f UTF-8       -i fil_PH $LOCALEDIR/ph_PH.UTF-8 || : 
localedef -c -f ISO-8859-15 -i fil_PH $LOCALEDIR/fil_PH.ISO-8859-15 || : 

#=========================================================

# aliases
for i in ja vi ; do
	case "$i" in
		ja) list="ja_JP.ujis" ;;
		*) list="" ;;
	esac

	for j in `echo $list` ;  do
		mkdir -p $LOCALEDIR/$j
		ln $LOCALEDIR/$i/LC_* $LOCALEDIR/$j || :
		mkdir $LOCALEDIR/$j/LC_MESSAGES
		ln $LOCALEDIR/$i/LC_MESSAGES/* $LOCALEDIR/$j/LC_MESSAGES || :
	done
done

# replace all identique files with hard links.
# script from Alastair McKinstry, 2000-07-03
cat > hardlink.pl << EOF
#!/usr/bin/perl
@files = \`find \$ARGV[0] -type f -a -not -name "LC_C*" \`;

foreach \$fi (@files) {
  chop (\$fi);
  (\$sum,\$name) = split(/ /,\`md5sum -b  \$fi\`);
  if (  \$orig{\$sum} eq "" ) {
    \$orig{\$sum} =\$fi;
  } else {
    \`ln -f \$orig{\$sum} \$fi\`;
  }
}
EOF
chmod a+x hardlink.pl
./hardlink.pl $RPM_BUILD_ROOT/usr/share/locale

# make LC_CTYPE and LC_COLLATE symlinks
cat > softlink.pl << EOF
#!/usr/bin/perl
@files = \`find [A-Z]* \$ARGV[0]* -type f -a -name "LC_C*" \`;

foreach \$fi (@files) {
  chop (\$fi);
  (\$sum,\$name) = split(/ /,\`md5sum -b  \$fi\`);
  if (  \$orig{\$sum} eq "" ) {
    \$orig{\$sum} =\$fi;
  } else {
    \`rm \$fi\`;
	\`ln -s ../\$orig{\$sum} \$fi\`;
  }
}
EOF
chmod a+x softlink.pl
(
 cd $RPM_BUILD_ROOT/usr/share/locale ;
 for i in `echo ?? ???`
 do
	LC_ALL=C $RPM_BUILD_DIR/locales-%{version}/softlink.pl $i
 done
)

cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%{loc_add} "UTF-8"
fi
%preun
if [ "$1" = "0" ]; then
	%{loc_del} "UTF-8"
fi

%files
%defattr(-,root,root)
%dir /usr/share/locale
/usr/share/locale/ISO*
/usr/share/locale/CP*
/usr/share/locale/UTF*
/usr/share/locale/KOI*
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
if [ "$1" = "1" ]; then
	%{loc_add} aa
fi
%preun -n locales-aa
if [ "$1" = "0" ]; then
	%{loc_del} aa
fi

%files -n locales-aa
%defattr(-,root,root)
/usr/share/locale/aa*

### af
# translation by Schalk Cronje <schalkc@ntaba.co.za>
%package -n locales-af
Summary: Base files for localization (Afrikaans)
Summary(af): Hierdie is die basislêers vir Afrikaanse lokalisasie
Group: System/Internationalization
URL: http://www.af.org.za/aflaai/linux-i18n/
Requires: locales = %{version}-%{release}

%description -n locales-af
These are the base files for Afrikaans language localization; you need
it to correctly display 8bits Afrikaans characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afrikaans language conventions.

%description -n locales-af -l af
Hierdie is die basislêers vir Afrikaanse lokalisasie. U benodig dit om die
Afrikaanse 8-bis karakters korrek te vertoon, vir korrekte alfabetiese
sorterting en ook om datums en getalle in die Afrikaanse standaardvorm te
vertoon.

%post -n locales-af
if [ "$1" = "1" ]; then
	%{loc_add} af
fi
%preun -n locales-af
if [ "$1" = "0" ]; then
	%{loc_del} af
fi

%files -n locales-af
%defattr(-,root,root)
/usr/share/locale/af*

### am
# translation by Daniel Yacob <Yacob@EthiopiaOnline.Net>
%package -n locales-am
Summary: Base files for localization (Amharic)
Summary(am): ለlocalization (አማርኛ) መሰረት ፋይሎች
Group: System/Internationalization
URL: http://www.ethiopic.org/
Requires: locales = %{version}-%{release}
Provides: locales-byn, locales-gez, locales-sid, locales-ti, locales-tig, locales-om, locales-wal

%description -n locales-am
These are the base files for Amharic language localization; you need
it to correctly display 8bits Amharic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amharic language conventions.

%description -n locales-am -l am
እነዚህ ያማርኛ ቋንቋ localization  መሰረት ፋይሎች ናቸው።
ያማርኛ ፊደላትንለማየት፣ የፊደላት ቅደም ተከተልን ለመጠበቅ፣
ቀኖችንና ቍጥሮችንበቋንቋው ስርዓት ለማስቀመጥ ያስፈልጋሉ።

%post -n locales-am
if [ "$1" = "1" ]; then
	%{loc_add} am byn ti gez sid tig om
fi
%preun -n locales-am
if [ "$1" = "0" ]; then
	%{loc_del} am byn ti gez sid tig om
fi

%files -n locales-am
%defattr(-,root,root)
/usr/share/locale/am*
# blin
/usr/share/locale/byn*
# tigrinya
# I can't use /usr/share/locale/ti* because of "tig"
/usr/share/locale/ti
/usr/share/locale/ti_*
# ge'ez
/usr/share/locale/gez*
# sidama
/usr/share/locale/sid*
# tigre
/usr/share/locale/tig*
# Oromo
/usr/share/locale/om*
# Walaita
/usr/share/locale/wal*

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
if [ "$1" = "1" ]; then
	%{loc_add} ar
fi
%preun -n locales-ar
if [ "$1" = "0" ]; then
	%{loc_del} ar
fi

%files -n locales-ar
%defattr(-,root,root)
/usr/share/locale/ar*

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
if [ "$1" = "1" ]; then
	%{loc_add} as
fi
%preun -n locales-as
if [ "$1" = "0" ]; then
	%{loc_del} as
fi

%files -n locales-as
%defattr(-,root,root)
/usr/share/locale/as*

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
if [ "$1" = "1" ]; then
	%{loc_add} az
fi
%preun -n locales-az
if [ "$1" = "0" ]; then
	%{loc_del} az
fi

%files -n locales-az
%defattr(-,root,root)
/usr/share/locale/az*

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
if [ "$1" = "1" ]; then
	%{loc_add} be
fi
%preun -n locales-be
if [ "$1" = "0" ]; then
	%{loc_del} be
fi

%files -n locales-be
%defattr(-,root,root)
# not just be* because of ber
/usr/share/locale/be
/usr/share/locale/be_*

### ber
%package -n locales-ber
Summary: Base files for localization (Berber)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-ber
These are the base files for Berber (Amazigh) language localization; you need
it to correctly display 8bits amazigh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amazigh language conventions.

%post -n locales-ber
if [ "$1" = "1" ]; then
	%{loc_add} ber
fi
%preun -n locales-ber
if [ "$1" = "0" ]; then
	%{loc_del} ber
fi

%files -n locales-ber
%defattr(-,root,root)
/usr/share/locale/ber*

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
if [ "$1" = "1" ]; then
	%{loc_add} bg
fi
%preun -n locales-bg
if [ "$1" = "0" ]; then
	%{loc_del} bg
fi

%files -n locales-bg
%defattr(-,root,root)
/usr/share/locale/bg*

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
if [ "$1" = "1" ]; then
	%{loc_add} bn
fi
%preun -n locales-bn
if [ "$1" = "0" ]; then
	%{loc_del} bn
fi

%files -n locales-bn
%defattr(-,root,root)
/usr/share/locale/bn*

### br
# Translation by Jañ-Mai Drapier (jan-mai-drapier@mail.dotcom.fr)
%package -n locales-br
Summary: Base files for localization (Breton)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue brétonne.
Summary(br): Kement-mañ a zo restroù diazez evit broelañ diouzh ar brezhoneg.

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
if [ "$1" = "1" ]; then
	%{loc_add} br
fi
%preun -n locales-br
if [ "$1" = "0" ]; then
	%{loc_del} br
fi

%files -n locales-br
%defattr(-,root,root)
/usr/share/locale/br*

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
if [ "$1" = "1" ]; then
	%{loc_add} bs
fi
%preun -n locales-bs
if [ "$1" = "0" ]; then
	%{loc_del} bs
fi

%files -n locales-bs
%defattr(-,root,root)
/usr/share/locale/bs*

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
if [ "$1" = "1" ]; then
	%{loc_add} ca
fi
%preun -n locales-ca
if [ "$1" = "0" ]; then
	%{loc_del} ca
fi

%files -n locales-ca
%defattr(-,root,root)
/usr/share/locale/ca*

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
if [ "$1" = "1" ]; then
	%{loc_add} cs
fi
%preun -n locales-cs
if [ "$1" = "0" ]; then
	%{loc_del} cs
fi

%files -n locales-cs
%defattr(-,root,root)
/usr/share/locale/cs*

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
if [ "$1" = "1" ]; then
	%{loc_add} cy
fi
%preun -n locales-cy
if [ "$1" = "0" ]; then
	%{loc_del} cy
fi

%files -n locales-cy
%defattr(-,root,root)
/usr/share/locale/cy*

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
if [ "$1" = "1" ]; then
	%{loc_add} da
fi
%preun -n locales-da
if [ "$1" = "0" ]; then
	%{loc_del} da
fi

%files -n locales-da
%defattr(-,root,root)
/usr/share/locale/da*

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
if [ "$1" = "1" ]; then
	%{loc_add} de
fi
%preun -n locales-de
if [ "$1" = "0" ]; then
	%{loc_del} de
fi

%files -n locales-de
%defattr(-,root,root)
/usr/share/locale/de*

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
if [ "$1" = "1" ]; then
	%{loc_add} dz
fi
%preun -n locales-dz
if [ "$1" = "0" ]; then
	%{loc_del} dz
fi

%files -n locales-dz
%defattr(-,root,root)
/usr/share/locale/dz*

### el
# translations from "Theodore J. Soldatos" <theodore@eexi.gr>
%package -n locales-el
Summary: Base files for localization (Greek)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: locales-gr
Provides: locales-gr
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
if [ "$1" = "1" ]; then
	%{loc_add} el
fi
%preun -n locales-el
if [ "$1" = "0" ]; then
	%{loc_del} el
fi

%files -n locales-el
%defattr(-,root,root)
/usr/share/locale/el*

### en
%package -n locales-en
Summary: Base files for localization (English)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-en_GB, locales-en_IE, locales-en_CA, locales-en_US

%description -n locales-en
These are the base files for English language localization.
Contains: en_CA en_DK en_GB en_IE en_US

%post -n locales-en
if [ "$1" = "1" ]; then
	%{loc_add} en en_GB en_IE en_US
fi
%preun -n locales-en
if [ "$1" = "0" ]; then
	%{loc_del} en en_GB en_IE en_US
fi

%files -n locales-en
%defattr(-,root,root)
/usr/share/locale/en*

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
if [ "$1" = "1" ]; then
	%{loc_add} eo
fi
%preun -n locales-eo
if [ "$1" = "0" ]; then
	%{loc_del} eo
fi

%files -n locales-eo
%defattr(-,root,root)
/usr/share/locale/eo*

### es
%package -n locales-es
Summary: Base files for localization (Spanish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(es): Ficheros de base para la localización (castellano)
Provides: locales-an

%description -n locales-es
These are the base files for Spanish language localization; you need
it to correctly display 8bits spanish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to spanish language conventions.

%description -n locales-es -l es
Este paquete incluye las definiciones de locales para el castellano.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del idioma español, para el orden alfabético 
y para la representación correcta de los números y fechas según 
las convenciones del castellano.

%post -n locales-es
if [ "$1" = "1" ]; then
	%{loc_add} es an
fi
%preun -n locales-es
if [ "$1" = "0" ]; then
	%{loc_del} es an
fi

%files -n locales-es
%defattr(-,root,root)
/usr/share/locale/es*
# Aragonese
/usr/share/locale/an*

### et
# translation from: Ekke Einberg <ekke@data.ee>
%package -n locales-et
Summary: Base files for localization (Estonian)
Summary(et): Siin on vajalikud failid Linuxi eestindamiseks.
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
if [ "$1" = "1" ]; then
	%{loc_add} et
fi
%preun -n locales-et
if [ "$1" = "0" ]; then
	%{loc_del} et
fi

%files -n locales-et
%defattr(-,root,root)
/usr/share/locale/et*

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
if [ "$1" = "1" ]; then
	%{loc_add} eu
fi
%preun -n locales-eu
if [ "$1" = "0" ]; then
	%{loc_del} eu
fi

%files -n locales-eu
%defattr(-,root,root)
/usr/share/locale/eu*

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
if [ "$1" = "1" ]; then
	%{loc_add} fa
fi
%preun -n locales-fa
if [ "$1" = "0" ]; then
	%{loc_del} fa
fi

%files -n locales-fa
%defattr(-,root,root)
/usr/share/locale/fa*

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
if [ "$1" = "1" ]; then
	%{loc_add} fi
fi
%preun -n locales-fi
if [ "$1" = "0" ]; then
	%{loc_del} fi
fi

%files -n locales-fi
%defattr(-,root,root)
# I can't use /usr/share/locale/fi* because of "fil"
/usr/share/locale/fi
/usr/share/locale/fi_*

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
if [ "$1" = "1" ]; then
	%{loc_add} fo
fi
%preun -n locales-fo
if [ "$1" = "0" ]; then
	%{loc_del} fo
fi

%files -n locales-fo
%defattr(-,root,root)
/usr/share/locale/fo*

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
if [ "$1" = "1" ]; then
	%{loc_add} fr
fi
%preun -n locales-fr
if [ "$1" = "0" ]; then
	%{loc_del} fr
fi

%files -n locales-fr
%defattr(-,root,root)
/usr/share/locale/fr*

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
if [ "$1" = "1" ]; then
	%{loc_add} fur
fi
%preun -n locales-fur
if [ "$1" = "0" ]; then
	%{loc_del} fur
fi

%files -n locales-fur
%defattr(-,root,root)
/usr/share/locale/fur*

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
if [ "$1" = "1" ]; then
	%{loc_add} fy
fi
%preun -n locales-fy
if [ "$1" = "0" ]; then
	%{loc_del} fy
fi

%files -n locales-fy
%defattr(-,root,root)
/usr/share/locale/fy*

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
if [ "$1" = "1" ]; then
	%{loc_add} ga
fi
%preun -n locales-ga
if [ "$1" = "0" ]; then
	%{loc_del} ga
fi

%files -n locales-ga
%defattr(-,root,root)
/usr/share/locale/ga*

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
if [ "$1" = "1" ]; then
	%{loc_add} gd
fi
%preun -n locales-gd
if [ "$1" = "0" ]; then
	%{loc_del} gd
fi

%files -n locales-gd
%defattr(-,root,root)
/usr/share/locale/gd*

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
if [ "$1" = "1" ]; then
	%{loc_add} gl
fi
%preun -n locales-gl
if [ "$1" = "0" ]; then
	%{loc_del} gl
fi

%files -n locales-gl
%defattr(-,root,root)
/usr/share/locale/gl*

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
if [ "$1" = "1" ]; then
	%{loc_add} gu
fi
%preun -n locales-gu
if [ "$1" = "0" ]; then
	%{loc_del} gu
fi

%files -n locales-gu
%defattr(-,root,root)
/usr/share/locale/gu*

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
if [ "$1" = "1" ]; then
	%{loc_add} gv
fi
%preun -n locales-gv
if [ "$1" = "0" ]; then
	%{loc_del} gv
fi

%files -n locales-gv
%defattr(-,root,root)
/usr/share/locale/gv*

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
if [ "$1" = "1" ]; then
	%{loc_add} ha
fi
%preun -n locales-ha
if [ "$1" = "0" ]; then
	%{loc_del} ha
fi

%files -n locales-ha
%defattr(-,root,root)
/usr/share/locale/ha*

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
if [ "$1" = "1" ]; then
	%{loc_add} he
fi
%preun -n locales-he
if [ "$1" = "0" ]; then
	%{loc_del} he
fi

%files -n locales-he
%defattr(-,root,root)
/usr/share/locale/he*

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
if [ "$1" = "1" ]; then
	%{loc_add} hi
fi
%preun -n locales-hi
if [ "$1" = "0" ]; then
	%{loc_del} hi
fi

%files -n locales-hi
%defattr(-,root,root)
/usr/share/locale/hi*

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
if [ "$1" = "1" ]; then
	%{loc_add} hr
fi
%preun -n locales-hr
if [ "$1" = "0" ]; then
	%{loc_del} hr
fi

%files -n locales-hr
%defattr(-,root,root)
/usr/share/locale/hr*

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
if [ "$1" = "1" ]; then
	%{loc_add} hsb
fi
%preun -n locales-hsb
if [ "$1" = "0" ]; then
	%{loc_del} hsb
fi

%files -n locales-hsb
%defattr(-,root,root)
/usr/share/locale/hsb*

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
if [ "$1" = "1" ]; then
	%{loc_add} hu
fi
%preun -n locales-hu
if [ "$1" = "0" ]; then
	%{loc_del} hu
fi

%files -n locales-hu
%defattr(-,root,root)
/usr/share/locale/hu*

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
if [ "$1" = "1" ]; then
	%{loc_add} hy
fi
%preun -n locales-hy
if [ "$1" = "0" ]; then
	%{loc_del} hy
fi

%files -n locales-hy
%defattr(-,root,root)
/usr/share/locale/hy*

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
if [ "$1" = "1" ]; then
	%{loc_add} id
fi
%preun -n locales-id
if [ "$1" = "0" ]; then
	%{loc_del} id
fi

%files -n locales-id
%defattr(-,root,root)
/usr/share/locale/id*

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
if [ "$1" = "1" ]; then
	%{loc_add} ig
fi
%preun -n locales-ig
if [ "$1" = "0" ]; then
	%{loc_del} ig
fi

%files -n locales-ig
%defattr(-,root,root)
/usr/share/locale/ig*

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
if [ "$1" = "1" ]; then
	%{loc_add} ik
fi
%preun -n locales-ik
if [ "$1" = "0" ]; then
	%{loc_del} ik
fi

%files -n locales-ik
%defattr(-,root,root)
/usr/share/locale/ik*

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
if [ "$1" = "1" ]; then
	%{loc_add} is
fi
%preun -n locales-is
if [ "$1" = "0" ]; then
	%{loc_del} is
fi

%files -n locales-is
%defattr(-,root,root)
# I can't use /usr/share/locale/is* because of /usr/share/locale/iso_8859_1
/usr/share/locale/is
/usr/share/locale/is_*

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
if [ "$1" = "1" ]; then
	%{loc_add} it
fi
%preun -n locales-it
if [ "$1" = "0" ]; then
	%{loc_del} it
fi

%files -n locales-it
%defattr(-,root,root)
/usr/share/locale/it*

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
if [ "$1" = "1" ]; then
	%{loc_add} iu
fi
%preun -n locales-iu
if [ "$1" = "0" ]; then
	%{loc_del} iu
fi

%files -n locales-iu
%defattr(-,root,root)
/usr/share/locale/iu*

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
if [ "$1" = "1" ]; then
	%{loc_add} ja
fi
%preun -n locales-ja
if [ "$1" = "0" ]; then
	%{loc_del} ja
fi

%files -n locales-ja
%defattr(-,root,root)
/usr/share/locale/ja*

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
if [ "$1" = "1" ]; then
	%{loc_add} ka
fi
%preun -n locales-ka
if [ "$1" = "0" ]; then
	%{loc_del} ka
fi

%files -n locales-ka
%defattr(-,root,root)
/usr/share/locale/ka*

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
if [ "$1" = "1" ]; then
	%{loc_add} kk
fi
%preun -n locales-kk
if [ "$1" = "0" ]; then
	%{loc_del} kk
fi

%files -n locales-kk
%defattr(-,root,root)
/usr/share/locale/kk*

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
if [ "$1" = "1" ]; then
	%{loc_add} kl
fi
%preun -n locales-kl
if [ "$1" = "0" ]; then
	%{loc_del} kl
fi

%files -n locales-kl
%defattr(-,root,root)
/usr/share/locale/kl*

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
if [ "$1" = "1" ]; then
	%{loc_add} km
fi
%preun -n locales-km
if [ "$1" = "0" ]; then
	%{loc_del} km
fi

%files -n locales-km
%defattr(-,root,root)
/usr/share/locale/km*

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
if [ "$1" = "1" ]; then
	%{loc_add} kn
fi
%preun -n locales-kn
if [ "$1" = "0" ]; then
	%{loc_del} kn
fi

%files -n locales-kn
%defattr(-,root,root)
/usr/share/locale/kn*

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
if [ "$1" = "1" ]; then
	%{loc_add} ko
fi
%preun -n locales-ko
if [ "$1" = "0" ]; then
	%{loc_del} ko
fi

%files -n locales-ko
%defattr(-,root,root)
/usr/share/locale/ko*

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
if [ "$1" = "1" ]; then
	%{loc_add} ku
fi
%preun -n locales-ku
if [ "$1" = "0" ]; then
	%{loc_del} ku
fi

%files -n locales-ku
%defattr(-,root,root)
/usr/share/locale/ku*

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
if [ "$1" = "1" ]; then
	%{loc_add} kw
fi
%preun -n locales-kw
if [ "$1" = "0" ]; then
	%{loc_del} kw
fi

%files -n locales-kw
%defattr(-,root,root)
/usr/share/locale/kw*

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
if [ "$1" = "1" ]; then
	%{loc_add} ky
fi
%preun -n locales-ky
if [ "$1" = "0" ]; then
	%{loc_del} ky
fi

%files -n locales-ky
%defattr(-,root,root)
/usr/share/locale/ky*

### lg
%package -n locales-lg
Summary: Base files for localization (Luganda)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-lug

%description -n locales-lg
These are the base files for Luganda (Ganda) language localization; you need
it to correctly display 8bits Luganda characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Luganda language conventions.

%post -n locales-lg
if [ "$1" = "1" ]; then
	%{loc_add} lg
fi
%preun -n locales-lg
if [ "$1" = "0" ]; then
	%{loc_del} lg
fi

%files -n locales-lg
%defattr(-,root,root)
/usr/share/locale/lg*

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
if [ "$1" = "1" ]; then
	%{loc_add} li
fi
%preun -n locales-li
if [ "$1" = "0" ]; then
	%{loc_del} li
fi

%files -n locales-li
%defattr(-,root,root)
/usr/share/locale/li*

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
if [ "$1" = "1" ]; then
	%{loc_add} lo
fi
%preun -n locales-lo
if [ "$1" = "0" ]; then
	%{loc_del} lo
fi

%files -n locales-lo
%defattr(-,root,root)
# not just lo* because of locale.alias
/usr/share/locale/lo
/usr/share/locale/lo_*

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
if [ "$1" = "1" ]; then
	%{loc_add} lt
fi
%preun -n locales-lt
if [ "$1" = "0" ]; then
	%{loc_del} lt
fi

%files -n locales-lt
%defattr(-,root,root)
# not just lt* because of ltg
/usr/share/locale/lt
/usr/share/locale/lt_*

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
if [ "$1" = "1" ]; then
	%{loc_add} lv
fi
%preun -n locales-lv
if [ "$1" = "0" ]; then
	%{loc_del} lv
fi

%files -n locales-lv
%defattr(-,root,root)
/usr/share/locale/lv*

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
if [ "$1" = "1" ]; then
	%{loc_add} mg
fi
%preun -n locales-mg
if [ "$1" = "0" ]; then
	%{loc_del} mg
fi

%files -n locales-mg
%defattr(-,root,root)
/usr/share/locale/mg*

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
if [ "$1" = "1" ]; then
	%{loc_add} mi
fi
%preun -n locales-mi
if [ "$1" = "0" ]; then
	%{loc_del} mi
fi

%files -n locales-mi
%defattr(-,root,root)
/usr/share/locale/mi*

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
if [ "$1" = "1" ]; then
	%{loc_add} mk
fi
%preun -n locales-mk
if [ "$1" = "0" ]; then
	%{loc_del} mk
fi

%files -n locales-mk
%defattr(-,root,root)
/usr/share/locale/mk*

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
if [ "$1" = "1" ]; then
	%{loc_add} ml
fi
%preun -n locales-ml
if [ "$1" = "0" ]; then
	%{loc_del} ml
fi

%files -n locales-ml
%defattr(-,root,root)
/usr/share/locale/ml*

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
if [ "$1" = "1" ]; then
	%{loc_add} mn
fi
%preun -n locales-mn
if [ "$1" = "0" ]; then
	%{loc_del} mn
fi

%files -n locales-mn
%defattr(-,root,root)
/usr/share/locale/mn*

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
if [ "$1" = "1" ]; then
	%{loc_add} mr
fi
%preun -n locales-mr
if [ "$1" = "0" ]; then
	%{loc_del} mr
fi

%files -n locales-mr
%defattr(-,root,root)
/usr/share/locale/mr*

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
if [ "$1" = "1" ]; then
	%{loc_add} ms
fi
%preun -n locales-ms
if [ "$1" = "0" ]; then
	%{loc_del} ms
fi

%files -n locales-ms
%defattr(-,root,root)
/usr/share/locale/ms*

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
if [ "$1" = "1" ]; then
	%{loc_add} mt
fi
%preun -n locales-mt
if [ "$1" = "0" ]; then
	%{loc_del} mt
fi

%files -n locales-mt
%defattr(-,root,root)
/usr/share/locale/mt*

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
if [ "$1" = "1" ]; then
	%{loc_add} nds
fi
%preun -n locales-nds
if [ "$1" = "0" ]; then
	%{loc_del} nds
fi

%files -n locales-nds
%defattr(-,root,root)
/usr/share/locale/nds*

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
if [ "$1" = "1" ]; then
	%{loc_add} ne
fi
%preun -n locales-ne
if [ "$1" = "0" ]; then
	%{loc_del} ne
fi

%files -n locales-ne
%defattr(-,root,root)
/usr/share/locale/ne*

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

description -n locales-nl -l nl
Dit zijn de basisbestanden nodig voor de Nederlandse taalmodule; ze zijn
noodzakelijk om de 8bits Nederlandse karakters correct weer te geven en
voor een juiste alfabetische sortering en weergave van data en nummers
volgens de Nederlandse Taalconventies

%post -n locales-nl
if [ "$1" = "1" ]; then
	%{loc_add} nl
fi
%preun -n locales-nl
if [ "$1" = "0" ]; then
	%{loc_del} nl
fi

%files -n locales-nl
%defattr(-,root,root)
/usr/share/locale/nl*

### no
# translations by peter@datadok.no
%package -n locales-no
Summary: Base files for localization (Norwegian)
Summary(nb): Dette er basisfilene for lokalisering til norsk språk
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-nn, locales-nb

%description -n locales-no
These are the base files for Norwegian language localization; you need
it to correctly display 8bits Norwegian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Norwegian language conventions.

%description -n locales-no -l nb
Dette er basisfilene for lokalisering til norsk språk. Du trenger dette
for å vise norske 8-bitstegn på riktig måte og for å få riktig sortering
etter alfabetet og visning av datoer og tall i samsvar med norske
konvensjoner.

%post -n locales-no
if [ "$1" = "1" ]; then
	%{loc_add} no nb nn
fi
%preun -n locales-no
if [ "$1" = "0" ]; then
	%{loc_del} no nb nn
fi

%files -n locales-no
%defattr(-,root,root)
/usr/share/locale/no*
/usr/share/locale/nb*
/usr/share/locale/nn*

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
if [ "$1" = "1" ]; then
	%{loc_add} nr
fi
%preun -n locales-nr
if [ "$1" = "0" ]; then
	%{loc_del} nr
fi

%files -n locales-nr
%defattr(-,root,root)
/usr/share/locale/nr*

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
if [ "$1" = "1" ]; then
	%{loc_add} nso
fi
%preun -n locales-nso
if [ "$1" = "0" ]; then
	%{loc_del} nso
fi

%files -n locales-nso
%defattr(-,root,root)
/usr/share/locale/nso*

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
if [ "$1" = "1" ]; then
	%{loc_add} oc
fi
%preun -n locales-oc
if [ "$1" = "0" ]; then
	%{loc_del} oc
fi

%files -n locales-oc
%defattr(-,root,root)
/usr/share/locale/oc*

### om
%package -n locales-om
Summary: Base files for localization (Oromo)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-om
These are the base files for Oromo language localization; you need
it to correctly display 8bits Oromo characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Oromo language conventions.

%post -n locales-om
if [ "$1" = "1" ]; then
	%{loc_add} om
fi
%preun -n locales-om
if [ "$1" = "0" ]; then
	%{loc_del} om
fi

#%files -n locales-om
#%defattr(-,root,root)
#/usr/share/locale/om*

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
if [ "$1" = "1" ]; then
	%{loc_add} pa
fi
%preun -n locales-pa
if [ "$1" = "0" ]; then
	%{loc_del} pa
fi

%files -n locales-pa
%defattr(-,root,root)
# not just pa* because of pap
/usr/share/locale/pa
/usr/share/locale/pa_*

### fil
# note: previously named "locales-ph"
%package -n locales-tl
Summary: Base files for localization (Pilipino)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-ph
Provides: locales-fil
Obsoletes: locales-ph

%description -n locales-tl
These are the base files for Pilipino (official language of the Philipines)
localization; you need it to correctly display 8bits characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Pilipino language conventions.

%post -n locales-tl
if [ "$1" = "1" ]; then
	%{loc_add} fil tl ph
fi
%preun -n locales-tl
if [ "$1" = "0" ]; then
	%{loc_del} fil tl ph
fi

%files -n locales-tl
%defattr(-,root,root)
/usr/share/locale/fil*
/usr/share/locale/ph*
/usr/share/locale/tl*

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
if [ "$1" = "1" ]; then
	%{loc_add} tn
fi
%preun -n locales-tn
if [ "$1" = "0" ]; then
	%{loc_del} tn
fi

%files -n locales-tn
%defattr(-,root,root)
/usr/share/locale/tn*

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
if [ "$1" = "1" ]; then
	%{loc_add} ts
fi
%preun -n locales-ts
if [ "$1" = "0" ]; then
	%{loc_del} ts
fi

%files -n locales-ts
%defattr(-,root,root)
/usr/share/locale/ts*

### pl
# translation from piotr pogorzelski <pp@pietrek.priv.pl>
%package -n locales-pl
Summary: Base files for localization (Polish)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Summary(pl): Podstawowe pliki dla polskiej lokalizacji

%description -n locales-pl
These are the base files for Polish language localization; you need
it to correctly display 8bits Polish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Polish language conventions.

%description -n locales-pl -l pl
Pliki do lokalizacji systemu dla języka polskiego. Niezbędne do poprawnego
wyświetlania 8-mio bitowych polskich znaków diakrytycznych, sortowania,
prezentowania dat i liczb zgodnie z regułami języka polskiego.

%post -n locales-pl
if [ "$1" = "1" ]; then
	%{loc_add} pl
fi
%preun -n locales-pl
if [ "$1" = "0" ]; then
	%{loc_del} pl
fi

%files -n locales-pl
%defattr(-,root,root)
/usr/share/locale/pl*

### pap
%package -n locales-pap
Summary: Base files for localization (Papiamento)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Obsoletes: locales-pp
Provides: locales-pp

%description -n locales-pap
These are the base files for Papiamento language localization; you need
it to correctly display 8bits Papiamento characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Papiamento language conventions.

%post -n locales-pap
if [ "$1" = "1" ]; then
	%{loc_add} pap
fi
%preun -n locales-pap
if [ "$1" = "0" ]; then
	%{loc_del} pap
fi

#%files -n locales-pap
#%defattr(-,root,root)
#/usr/share/locale/pap*

### pt
%package -n locales-pt
Summary: Base files for localization (Portuguese)
Summary(pt): Estes são os arquivos básicos para a localização (Português)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-pt_BR, locales-pt_PT

%description -n locales-pt
These are the base files for Portuguese language localization; you need
it to correctly display 8bits Portuguese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Portuguese language conventions.

%description -n locales-pt -l pt
Estes são os arquivos básicos para a localização lingüística em português;
eles são necessários para que o sistema mostre corretamente caracteres
portugueses de 8 bits, e para que tenha as apropriadas ordenações
alfabéticas e representação de datas e números de acordo com as convenções
da língua portuguesa.

%post -n locales-pt
if [ "$1" = "1" ]; then
	%{loc_add} pt pt_BR pt_PT
fi
%preun -n locales-pt
if [ "$1" = "0" ]; then
	%{loc_del} pt pt_BR pt_PT
fi

%files -n locales-pt
%defattr(-,root,root)
/usr/share/locale/pt*

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
if [ "$1" = "1" ]; then
	%{loc_add} ro
fi
%preun -n locales-ro
if [ "$1" = "0" ]; then
	%{loc_del} ro
fi

%files -n locales-ro
%defattr(-,root,root)
/usr/share/locale/ro*

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
if [ "$1" = "1" ]; then
	%{loc_add} ru
fi
%preun -n locales-ru
if [ "$1" = "0" ]; then
	%{loc_del} ru
fi

%files -n locales-ru
%defattr(-,root,root)
/usr/share/locale/ru*

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
if [ "$1" = "1" ]; then
	%{loc_add} rw
fi
%preun -n locales-rw
if [ "$1" = "0" ]; then
	%{loc_del} rw
fi

%files -n locales-rw
%defattr(-,root,root)
/usr/share/locale/rw*

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
if [ "$1" = "1" ]; then
	%{loc_add} sc
fi
%preun -n locales-sc
if [ "$1" = "0" ]; then
	%{loc_del} sc
fi

%files -n locales-sc
%defattr(-,root,root)
/usr/share/locale/sc*

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
if [ "$1" = "1" ]; then
	%{loc_add} se
fi
%preun -n locales-se
if [ "$1" = "0" ]; then
	%{loc_del} se
fi

%files -n locales-se
%defattr(-,root,root)
/usr/share/locale/se*

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
if [ "$1" = "1" ]; then
	%{loc_add} si
fi
%preun -n locales-si
if [ "$1" = "0" ]; then
	%{loc_del} si
fi

%files -n locales-si
%defattr(-,root,root)
# I can't use /usr/share/locale/si* because of "sid"
/usr/share/locale/si
/usr/share/locale/si_*

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
if [ "$1" = "1" ]; then
	%{loc_add} sk
fi
%preun -n locales-sk
if [ "$1" = "0" ]; then
	%{loc_del} sk
fi

%files -n locales-sk
%defattr(-,root,root)
/usr/share/locale/sk*

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
if [ "$1" = "1" ]; then
	%{loc_add} sl
fi
%preun -n locales-sl
if [ "$1" = "0" ]; then
	%{loc_del} sl
fi

%files -n locales-sl
%defattr(-,root,root)
/usr/share/locale/sl*

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
if [ "$1" = "1" ]; then
	%{loc_add} so
fi
%preun -n locales-so
if [ "$1" = "0" ]; then
	%{loc_del} so
fi

%files -n locales-so
%defattr(-,root,root)
/usr/share/locale/so*

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
if [ "$1" = "1" ]; then
	%{loc_add} sq
fi
%preun -n locales-sq
if [ "$1" = "0" ]; then
	%{loc_del} sq
fi

%files -n locales-sq
%defattr(-,root,root)
/usr/share/locale/sq*

### sr
%package -n locales-sr
Summary: Base files for localization (Serbian)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-sh, locales-sr@Latn
Summary(sr): Основне датотеке за локализацију (Српски) 
Summary(sr@Latn): Osnovne datoteke za lokalizaciju (Srpski)
Summary(sh): Osnovne datoteke za lokalizaciju (Srpski)

%description -n locales-sr
These are the base files for Serbian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Serbian language conventions.

%description -n locales-sr -l sr
Ово су основне датотеке за
локализацију на Српски језик; потребне
су да се правилно приказали 8 битни
Српски знакови, за правилно
сортирање по абецеди и приказ датума
и бројева по правилима Српског језика.

%description -n locales-sr -l sr@Latn
Ovo su osnovne datoteke za
lokalizaciju na Srpski jezik; potrebne
su da se pravilno prikazali 8 bitni
Srpski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma
i brojeva po pravilima Srpskog jezika.

%description -n locales-sr -l sh
Ovo su osnovne datoteke za
lokalizaciju na Srpski jezik; potrebne
su da se pravilno prikazali 8 bitni
Srpski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma
i brojeva po pravilima Srpskog jezika.

%post -n locales-sr
if [ "$1" = "1" ]; then
	%{loc_add} sr sr@Latn sh
fi
%preun -n locales-sr
if [ "$1" = "0" ]; then
	%{loc_del} sr sr@Latn sh
fi

%files -n locales-sr
%defattr(-,root,root)
/usr/share/locale/sh*
/usr/share/locale/sr*

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
if [ "$1" = "1" ]; then
	%{loc_add} ss
fi
%preun -n locales-ss
if [ "$1" = "0" ]; then
	%{loc_del} ss
fi

%files -n locales-ss
%defattr(-,root,root)
/usr/share/locale/ss*

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
if [ "$1" = "1" ]; then
	%{loc_add} st
fi
%preun -n locales-st
if [ "$1" = "0" ]; then
	%{loc_del} st
fi

%files -n locales-st
%defattr(-,root,root)
/usr/share/locale/st*

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
if [ "$1" = "1" ]; then
	%{loc_add} sv
fi
%preun -n locales-sv
if [ "$1" = "0" ]; then
	%{loc_del} sv
fi

%files -n locales-sv
%defattr(-,root,root)
/usr/share/locale/sv*

### sw
%package -n locales-sw
Summary: Base files for localization (Swahili)
Group: System/Internationalization
Requires: locales = %{version}-%{release}

%description -n locales-sw
These are the base files for Swahili language localization; you need
it to correctly display 8bits Swahili characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swahili language conventions.

%post -n locales-sw
if [ "$1" = "1" ]; then
	%{loc_add} sw
fi
%preun -n locales-sw
if [ "$1" = "0" ]; then
	%{loc_del} sw
fi

%files -n locales-sw
%defattr(-,root,root)
/usr/share/locale/sw*

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
if [ "$1" = "1" ]; then
	%{loc_add} ta
fi
%preun -n locales-ta
if [ "$1" = "0" ]; then
	%{loc_del} ta
fi

%files -n locales-ta
%defattr(-,root,root)
/usr/share/locale/ta*

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
if [ "$1" = "1" ]; then
	%{loc_add} te
fi
%preun -n locales-te
if [ "$1" = "0" ]; then
	%{loc_del} te
fi

%files -n locales-te
%defattr(-,root,root)
/usr/share/locale/te*

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
if [ "$1" = "1" ]; then
	%{loc_add} tg
fi
%preun -n locales-tg
if [ "$1" = "0" ]; then
	%{loc_del} tg
fi

%files -n locales-tg
%defattr(-,root,root)
/usr/share/locale/tg*

### th
%package -n locales-th
Summary: Base files for localization (Thai)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
URL: http://www.links.nectec.or.th/~thep/th-locale/

%description -n locales-th
These are the base files for Thai language localization; you need
it to correctly display 8bits Thai characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Thai language conventions.

%post -n locales-th
if [ "$1" = "1" ]; then
	%{loc_add} th
fi
%preun -n locales-th
if [ "$1" = "0" ]; then
	%{loc_del} th
fi

%files -n locales-th
%defattr(-,root,root)
/usr/share/locale/th*

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
if [ "$1" = "1" ]; then
	%{loc_add} tk
fi
%preun -n locales-tk
if [ "$1" = "0" ]; then
	%{loc_del} tk
fi

%files -n locales-tk
%defattr(-,root,root)
/usr/share/locale/tk*

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
if [ "$1" = "1" ]; then
	%{loc_add} tr
fi
%preun -n locales-tr
if [ "$1" = "0" ]; then
	%{loc_del} tr
fi

%files -n locales-tr
%defattr(-,root,root)
/usr/share/locale/tr*

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
if [ "$1" = "1" ]; then
	%{loc_add} tt
fi
%preun -n locales-tt
if [ "$1" = "0" ]; then
	%{loc_del} tt
fi

%files -n locales-tt
%defattr(-,root,root)
/usr/share/locale/tt*

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
if [ "$1" = "1" ]; then
	%{loc_add} ug
fi
%preun -n locales-ug
if [ "$1" = "0" ]; then
	%{loc_del} ug
fi

%files -n locales-ug
%defattr(-,root,root)
/usr/share/locale/ug*

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
if [ "$1" = "1" ]; then
	%{loc_add} uk
fi
%preun -n locales-uk
if [ "$1" = "0" ]; then
	%{loc_del} uk
fi

%files -n locales-uk
%defattr(-,root,root)
/usr/share/locale/uk*

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
if [ "$1" = "1" ]; then
	%{loc_add} ur
fi
%preun -n locales-ur
if [ "$1" = "0" ]; then
	%{loc_del} ur
fi

%files -n locales-ur
%defattr(-,root,root)
/usr/share/locale/ur*

### uz
%package -n locales-uz
Summary: Base files for localization (Uzbek)
Summary(uz): Lokallashtirishning asosiy fayllari (o'zbekcha)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-uz@Latn

%description -n locales-uz
These are the base files for Uzbek language localization; you need
it to correctly display 8bits Uzbek characters, and for proper
alphabetical sorting and representation of dates and numbers
according to Uzbek language conventions.

%description -n locales-uz -l uz
Ushbu asos fayllar Linuxni o'zbekchaga locallashtirish
uchun qo'llaniladi; siz bularni 8 bit o'zbek
harflarini to'g'ri ko'rish va tartiblashda qollanasiz.
O'zbekistonda joriy bo'lgan vaqt, son va valytani
belgilash qoidalari ham shu fayllarda joylashgan.

%post -n locales-uz
if [ "$1" = "1" ]; then
	%{loc_add} uz uz@Latn
fi
%preun -n locales-uz
if [ "$1" = "0" ]; then
	%{loc_del} uz uz@Latn
fi

%files -n locales-uz
%defattr(-,root,root)
/usr/share/locale/uz*

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
if [ "$1" = "1" ]; then
	%{loc_add} ve
fi
%preun -n locales-ve
if [ "$1" = "0" ]; then
	%{loc_del} ve
fi

%files -n locales-ve
%defattr(-,root,root)
/usr/share/locale/ve*

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
if [ "$1" = "1" ]; then
	%{loc_add} vi
fi
%preun -n locales-vi
if [ "$1" = "0" ]; then
	%{loc_del} vi
fi

%files -n locales-vi
%defattr(-,root,root)
/usr/share/locale/vi*

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
if [ "$1" = "1" ]; then
	%{loc_add} wa
fi
%preun -n locales-wa
if [ "$1" = "0" ]; then
	%{loc_del} wa
fi

%files -n locales-wa
%defattr(-,root,root)
# I can't use /usr/share/locale/wa* because of "war"
/usr/share/locale/wa
/usr/share/locale/wa_*

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
if [ "$1" = "1" ]; then
	%{loc_add} xh
fi
%preun -n locales-xh
if [ "$1" = "0" ]; then
	%{loc_del} xh
fi

%files -n locales-xh
%defattr(-,root,root)
/usr/share/locale/xh*

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
if [ "$1" = "1" ]; then
	%{loc_add} yi
fi
%preun -n locales-yi
if [ "$1" = "0" ]; then
	%{loc_del} yi
fi

%files -n locales-yi
%defattr(-,root,root)
/usr/share/locale/yi*

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
if [ "$1" = "1" ]; then
	%{loc_add} yo
fi
%preun -n locales-yo
if [ "$1" = "0" ]; then
	%{loc_del} yo
fi

%files -n locales-yo
%defattr(-,root,root)
/usr/share/locale/yo*

### zh
# translation (zh_TW) from <informer@linux1.cgu.edu.tw>
# zh_CN converted from zh_TW.Big5 with b5togb; corrections welcome.
%package -n locales-zh
Summary: Base files for localization (Chinese)
Group: System/Internationalization
Requires: locales = %{version}-%{release}
Provides: locales-zh_CN, locales-zh_TW, locales-zh_SG, locales-zh_HK
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
if [ "$1" = "1" ]; then
	%{loc_add} zh zh_CN zh_TW zh_SG zh_HK
fi
%preun -n locales-zh
if [ "$1" = "0" ]; then
	%{loc_del} zh zh_CN zh_TW zh_SG zh_HK
fi

%files -n locales-zh
%defattr(-,root,root)
/usr/share/locale/zh*

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
if [ "$1" = "1" ]; then
	%{loc_add} zu
fi
%preun -n locales-zu
if [ "$1" = "0" ]; then
	%{loc_del} zu
fi

%files -n locales-zu
%defattr(-,root,root)
/usr/share/locale/zu*
