const countries_codes = [
  ["Afghanistan", "93"],
  ["Albania", "355"],
  ["Algeria", "213"],
  ["American Samoa", "1-684"],
  ["Andorra", "376"],
  ["Angola", "244"],
  ["Anguilla", "1-264"],
  ["Antarctica", "672"],
  ["Antigua and Barbuda", "1-268"],
  ["Argentina", "54"],
  ["Armenia", "374"],
  ["Aruba", "297"],
  ["Australia", "61"],
  ["Austria", "43"],
  ["Azerbaijan", "994"],
  ["Bahamas", "1-242"],
  ["Bahrain", "973"],
  ["Bangladesh", "880"],
  ["Barbados", "1-246"],
  ["Belarus", "375"],
  ["Belgium", "32"],
  ["Belize", "501"],
  ["Benin", "229"],
  ["Bermuda", "1-441"],
  ["Bhutan", "975"],
  ["Bolivia", "591"],
  ["Bosnia and Herzegovina", "387"],
  ["Botswana", "267"],
  ["Brazil", "55"],
  ["British Indian Ocean Territory", "246"],
  ["British Virgin Islands", "1-284"],
  ["Brunei", "673"],
  ["Bulgaria", "359"],
  ["Burkina Faso", "226"],
  ["Myanmar", "95"],
  ["Burundi", "257"],
  ["Cambodia", "855"],
  ["Cameroon", "237"],
  ["Canada", "1"],
  ["Cape Verde", "238"],
  ["Cayman Islands", "1-345"],
  ["Central African Republic", "236"],
  ["Chad", "235"],
  ["Chile", "56"],
  ["China", "86"],
  ["Christmas Island", "61"],
  ["Cocos Islands", "61"],
  ["Colombia", "57"],
  ["Comoros", "269"],
  ["Republic of the Congo", "242"],
  ["Democratic Republic of the Congo", "243"],
  ["Cook Islands", "682"],
  ["Costa Rica", "506"],
  ["Croatia", "385"],
  ["Cuba", "53"],
  ["Curacao", "599"],
  ["Cyprus", "357"],
  ["Czech Republic", "420"],
  ["Denmark", "45"],
  ["Djibouti", "253"],
  ["Dominica", "1-767"],
  ["Dominican Republic", "1-809, 1-829, 1-849"],
  ["East Timor", "670"],
  ["Ecuador", "593"],
  ["Egypt", "20"],
  ["El Salvador", "503"],
  ["Equatorial Guinea", "240"],
  ["Eritrea", "291"],
  ["Estonia", "372"],
  ["Ethiopia", "251"],
  ["Falkland Islands", "500"],
  ["Faroe Islands", "298"],
  ["Fiji", "679"],
  ["Finland", "358"],
  ["France", "33"],
  ["French Polynesia", "689"],
  ["Gabon", "241"],
  ["Gambia", "220"],
  ["Georgia", "995"],
  ["Germany", "49"],
  ["Ghana", "233"],
  ["Gibraltar", "350"],
  ["Greece", "30"],
  ["Greenland", "299"],
  ["Grenada", "1-473"],
  ["Guam", "1-671"],
  ["Guatemala", "502"],
  ["Guernsey", "44-1481"],
  ["Guinea", "224"],
  ["Guinea-Bissau", "245"],
  ["Guyana", "592"],
  ["Haiti", "509"],
  ["Honduras", "504"],
  ["Hong Kong", "852"],
  ["Hungary", "36"],
  ["Iceland", "354"],
  ["India", "91"],
  ["Indonesia", "62"],
  ["Iran", "98"],
  ["Iraq", "964"],
  ["Ireland", "353"],
  ["Isle of Man", "44-1624"],
  ["Israel", "972"],
  ["Italy", "39"],
  ["Ivory Coast", "225"],
  ["Jamaica", "1-876"],
  ["Japan", "81"],
  ["Jersey", "44-1534"],
  ["Jordan", "962"],
  ["Kazakhstan", "7"],
  ["Kenya", "254"],
  ["Kiribati", "686"],
  ["Kosovo", "383"],
  ["Kuwait", "965"],
  ["Kyrgyzstan", "996"],
  ["Laos", "856"],
  ["Latvia", "371"],
  ["Lebanon", "961"],
  ["Lesotho", "266"],
  ["Liberia", "231"],
  ["Libya", "218"],
  ["Liechtenstein", "423"],
  ["Lithuania", "370"],
  ["Luxembourg", "352"],
  ["Macau", "853"],
  ["Macedonia", "389"],
  ["Madagascar", "261"],
  ["Malawi", "265"],
  ["Malaysia", "60"],
  ["Maldives", "960"],
  ["Mali", "223"],
  ["Malta", "356"],
  ["Marshall Islands", "692"],
  ["Mauritania", "222"],
  ["Mauritius", "230"],
  ["Mayotte", "262"],
  ["México", "52"],
  ["Micronesia", "691"],
  ["Moldova", "373"],
  ["Monaco", "377"],
  ["Mongolia", "976"],
  ["Montenegro", "382"],
  ["Montserrat", "1-664"],
  ["Morocco", "212"],
  ["Mozambique", "258"],
  ["Namibia", "264"],
  ["Nauru", "674"],
  ["Nepal", "977"],
  ["Netherlands", "31"],
  ["Netherlands Antilles", "599"],
  ["New Caledonia", "687"],
  ["New Zealand", "64"],
  ["Nicaragua", "505"],
  ["Niger", "227"],
  ["Nigeria", "234"],
  ["Niue", "683"],
  ["Northern Mariana Islands", "1-670"],
  ["North Korea", "850"],
  ["Norway", "47"],
  ["Oman", "968"],
  ["Pakistan", "92"],
  ["Palau", "680"],
  ["Palestine", "970"],
  ["Panama", "507"],
  ["Papua New Guinea", "675"],
  ["Paraguay", "595"],
  ["Peru", "51"],
  ["Philippines", "63"],
  ["Pitcairn", "64"],
  ["Poland", "48"],
  ["Portugal", "351"],
  ["Puerto Rico", "1-787, 1-939"],
  ["Qatar", "974"],
  ["Reunion", "262"],
  ["Romania", "40"],
  ["Russia", "7"],
  ["Rwanda", "250"],
  ["Saint Barthelemy", "590"],
  ["Samoa", "685"],
  ["San Marino", "378"],
  ["Sao Tome and Principe", "239"],
  ["Saudi Arabia", "966"],
  ["Senegal", "221"],
  ["Serbia", "381"],
  ["Seychelles", "248"],
  ["Sierra Leone", "232"],
  ["Singapore", "65"],
  ["Sint Maarten", "1-721"],
  ["Slovakia", "421"],
  ["Slovenia", "386"],
  ["Solomon Islands", "677"],
  ["Somalia", "252"],
  ["South Africa", "27"],
  ["South Korea", "82"],
  ["South Sudan", "211"],
  ["Spain", "34"],
  ["Sri Lanka", "94"],
  ["Saint Helena", "290"],
  ["Saint Kitts and Nevis", "1-869"],
  ["Saint Lucia", "1-758"],
  ["Saint Martin", "590"],
  ["Saint Pierre and Miquelon", "508"],
  ["Saint Vincent and the Grenadines", "1-784"],
  ["Sudan", "249"],
  ["Suriname", "597"],
  ["Svalbard and Jan Mayen", "47"],
  ["Swaziland", "268"],
  ["Sweden", "46"],
  ["Switzerland", "41"],
  ["Syria", "963"],
  ["Taiwan", "886"],
  ["Tajikistan", "992"],
  ["Tanzania", "255"],
  ["Thailand", "66"],
  ["Togo", "228"],
  ["Tokelau", "690"],
  ["Tonga", "676"],
  ["Trinidad and Tobago", "1-868"],
  ["Tunisia", "216"],
  ["Turkey", "90"],
  ["Turkmenistan", "993"],
  ["Turks and Caicos Islands", "1-649"],
  ["Tuvalu", "688"],
  ["United Arab Emirates", "971"],
  ["Uganda", "256"],
  ["United Kingdom", "44"],
  ["Ukraine", "380"],
  ["Uruguay", "598"],
  ["United States", "1"],
  ["Uzbekistan", "998"],
  ["Vanuatu", "678"],
  ["Vatican", "379"],
  ["Venezuela", "58"],
  ["Vietnam", "84"],
  ["U.S. Virgin Islands", "1-340"],
  ["Wallis and Futuna", "681"],
  ["Western Sahara", "212"],
  ["Yemen", "967"],
  ["Zambia", "260"],
  ["Zimbabwe", "263"],
]

const time_zones = [
  "Africa/Abidjan",
  "Africa/Accra",
  "Africa/Addis_Ababa",
  "Africa/Algiers",
  "Africa/Asmara",
  "Africa/Asmera",
  "Africa/Bamako",
  "Africa/Bangui",
  "Africa/Banjul",
  "Africa/Bissau",
  "Africa/Blantyre",
  "Africa/Brazzaville",
  "Africa/Bujumbura",
  "Africa/Cairo",
  "Africa/Casablanca",
  "Africa/Ceuta",
  "Africa/Conakry",
  "Africa/Dakar",
  "Africa/Dar_es_Salaam",
  "Africa/Djibouti",
  "Africa/Douala",
  "Africa/El_Aaiun",
  "Africa/Freetown",
  "Africa/Gaborone",
  "Africa/Harare",
  "Africa/Johannesburg",
  "Africa/Juba",
  "Africa/Kampala",
  "Africa/Khartoum",
  "Africa/Kigali",
  "Africa/Kinshasa",
  "Africa/Lagos",
  "Africa/Libreville",
  "Africa/Lome",
  "Africa/Luanda",
  "Africa/Lubumbashi",
  "Africa/Lusaka",
  "Africa/Malabo",
  "Africa/Maputo",
  "Africa/Maseru",
  "Africa/Mbabane",
  "Africa/Mogadishu",
  "Africa/Monrovia",
  "Africa/Nairobi",
  "Africa/Ndjamena",
  "Africa/Niamey",
  "Africa/Nouakchott",
  "Africa/Ouagadougou",
  "Africa/Porto-Novo",
  "Africa/Sao_Tome",
  "Africa/Timbuktu",
  "Africa/Tripoli",
  "Africa/Tunis",
  "Africa/Windhoek",
  "America/Adak",
  "America/Anchorage",
  "America/Anguilla",
  "America/Antigua",
  "America/Araguaina",
  "America/Argentina/Buenos_Aires",
  "America/Argentina/Catamarca",
  "America/Argentina/ComodRivadavia",
  "America/Argentina/Cordoba",
  "America/Argentina/Jujuy",
  "America/Argentina/La_Rioja",
  "America/Argentina/Mendoza",
  "America/Argentina/Rio_Gallegos",
  "America/Argentina/Salta",
  "America/Argentina/San_Juan",
  "America/Argentina/San_Luis",
  "America/Argentina/Tucuman",
  "America/Argentina/Ushuaia",
  "America/Aruba",
  "America/Asuncion",
  "America/Atikokan",
  "America/Atka",
  "America/Bahia",
  "America/Bahia_Banderas",
  "America/Barbados",
  "America/Belem",
  "America/Belize",
  "America/Blanc-Sablon",
  "America/Boa_Vista",
  "America/Bogota",
  "America/Boise",
  "America/Buenos_Aires",
  "America/Cambridge_Bay",
  "America/Campo_Grande",
  "America/Cancun",
  "America/Caracas",
  "America/Catamarca",
  "America/Cayenne",
  "America/Cayman",
  "America/Chicago",
  "America/Chihuahua",
  "America/Coral_Harbour",
  "America/Cordoba",
  "America/Costa_Rica",
  "America/Creston",
  "America/Cuiaba",
  "America/Curacao",
  "America/Danmarkshavn",
  "America/Dawson",
  "America/Dawson_Creek",
  "America/Denver",
  "America/Detroit",
  "America/Dominica",
  "America/Edmonton",
  "America/Eirunepe",
  "America/El_Salvador",
  "America/Ensenada",
  "America/Fort_Wayne",
  "America/Fortaleza",
  "America/Glace_Bay",
  "America/Godthab",
  "America/Goose_Bay",
  "America/Grand_Turk",
  "America/Grenada",
  "America/Guadeloupe",
  "America/Guatemala",
  "America/Guayaquil",
  "America/Guyana",
  "America/Halifax",
  "America/Havana",
  "America/Hermosillo",
  "America/Indiana/Indianapolis",
  "America/Indiana/Knox",
  "America/Indiana/Marengo",
  "America/Indiana/Petersburg",
  "America/Indiana/Tell_City",
  "America/Indiana/Vevay",
  "America/Indiana/Vincennes",
  "America/Indiana/Winamac",
  "America/Indianapolis",
  "America/Inuvik",
  "America/Iqaluit",
  "America/Jamaica",
  "America/Jujuy",
  "America/Juneau",
  "America/Kentucky/Louisville",
  "America/Kentucky/Monticello",
  "America/Knox_IN",
  "America/Kralendijk",
  "America/La_Paz",
  "America/Lima",
  "America/Los_Angeles",
  "America/Louisville",
  "America/Lower_Princes",
  "America/Maceio",
  "America/Managua",
  "America/Manaus",
  "America/Marigot",
  "America/Martinique",
  "America/Matamoros",
  "America/Mazatlan",
  "America/Mendoza",
  "America/Menominee",
  "America/Merida",
  "America/Metlakatla",
  "America/Mexico_City",
  "America/Miquelon",
  "America/Moncton",
  "America/Monterrey",
  "America/Montevideo",
  "America/Montreal",
  "America/Montserrat",
  "America/Nassau",
  "America/New_York",
  "America/Nipigon",
  "America/Nome",
  "America/Noronha",
  "America/North_Dakota/Beulah",
  "America/North_Dakota/Center",
  "America/North_Dakota/New_Salem",
  "America/Ojinaga",
  "America/Panama",
  "America/Pangnirtung",
  "America/Paramaribo",
  "America/Phoenix",
  "America/Port-au-Prince",
  "America/Port_of_Spain",
  "America/Porto_Acre",
  "America/Porto_Velho",
  "America/Puerto_Rico",
  "America/Rainy_River",
  "America/Rankin_Inlet",
  "America/Recife",
  "America/Regina",
  "America/Resolute",
  "America/Rio_Branco",
  "America/Rosario",
  "America/Santa_Isabel",
  "America/Santarem",
  "America/Santiago",
  "America/Santo_Domingo",
  "America/Sao_Paulo",
  "America/Scoresbysund",
  "America/Shiprock",
  "America/Sitka",
  "America/St_Barthelemy",
  "America/St_Johns",
  "America/St_Kitts",
  "America/St_Lucia",
  "America/St_Thomas",
  "America/St_Vincent",
  "America/Swift_Current",
  "America/Tegucigalpa",
  "America/Thule",
  "America/Thunder_Bay",
  "America/Tijuana",
  "America/Toronto",
  "America/Tortola",
  "America/Vancouver",
  "America/Virgin",
  "America/Whitehorse",
  "America/Winnipeg",
  "America/Yakutat",
  "America/Yellowknife",
  "Antarctica/Casey",
  "Antarctica/Davis",
  "Antarctica/DumontDUrville",
  "Antarctica/Macquarie",
  "Antarctica/Mawson",
  "Antarctica/McMurdo",
  "Antarctica/Palmer",
  "Antarctica/Rothera",
  "Antarctica/South_Pole",
  "Antarctica/Syowa",
  "Antarctica/Vostok",
  "Arctic/Longyearbyen",
  "Asia/Aden",
  "Asia/Almaty",
  "Asia/Amman",
  "Asia/Anadyr",
  "Asia/Aqtau",
  "Asia/Aqtobe",
  "Asia/Ashgabat",
  "Asia/Ashkhabad",
  "Asia/Baghdad",
  "Asia/Bahrain",
  "Asia/Baku",
  "Asia/Bangkok",
  "Asia/Beirut",
  "Asia/Bishkek",
  "Asia/Brunei",
  "Asia/Calcutta",
  "Asia/Choibalsan",
  "Asia/Chongqing",
  "Asia/Chungking",
  "Asia/Colombo",
  "Asia/Dacca",
  "Asia/Damascus",
  "Asia/Dhaka",
  "Asia/Dili",
  "Asia/Dubai",
  "Asia/Dushanbe",
  "Asia/Gaza",
  "Asia/Harbin",
  "Asia/Hebron",
  "Asia/Ho_Chi_Minh",
  "Asia/Hong_Kong",
  "Asia/Hovd",
  "Asia/Irkutsk",
  "Asia/Istanbul",
  "Asia/Jakarta",
  "Asia/Jayapura",
  "Asia/Jerusalem",
  "Asia/Kabul",
  "Asia/Kamchatka",
  "Asia/Karachi",
  "Asia/Kashgar",
  "Asia/Kathmandu",
  "Asia/Katmandu",
  "Asia/Khandyga",
  "Asia/Kolkata",
  "Asia/Krasnoyarsk",
  "Asia/Kuala_Lumpur",
  "Asia/Kuching",
  "Asia/Kuwait",
  "Asia/Macao",
  "Asia/Macau",
  "Asia/Magadan",
  "Asia/Makassar",
  "Asia/Manila",
  "Asia/Muscat",
  "Asia/Nicosia",
  "Asia/Novokuznetsk",
  "Asia/Novosibirsk",
  "Asia/Omsk",
  "Asia/Oral",
  "Asia/Phnom_Penh",
  "Asia/Pontianak",
  "Asia/Pyongyang",
  "Asia/Qatar",
  "Asia/Qyzylorda",
  "Asia/Rangoon",
  "Asia/Riyadh",
  "Asia/Saigon",
  "Asia/Sakhalin",
  "Asia/Samarkand",
  "Asia/Seoul",
  "Asia/Shanghai",
  "Asia/Singapore",
  "Asia/Taipei",
  "Asia/Tashkent",
  "Asia/Tbilisi",
  "Asia/Tehran",
  "Asia/Tel_Aviv",
  "Asia/Thimbu",
  "Asia/Thimphu",
  "Asia/Tokyo",
  "Asia/Ujung_Pandang",
  "Asia/Ulaanbaatar",
  "Asia/Ulan_Bator",
  "Asia/Urumqi",
  "Asia/Ust-Nera",
  "Asia/Vientiane",
  "Asia/Vladivostok",
  "Asia/Yakutsk",
  "Asia/Yekaterinburg",
  "Asia/Yerevan",
  "Atlantic/Azores",
  "Atlantic/Bermuda",
  "Atlantic/Canary",
  "Atlantic/Cape_Verde",
  "Atlantic/Faeroe",
  "Atlantic/Faroe",
  "Atlantic/Jan_Mayen",
  "Atlantic/Madeira",
  "Atlantic/Reykjavik",
  "Atlantic/South_Georgia",
  "Atlantic/St_Helena",
  "Atlantic/Stanley",
  "Australia/ACT",
  "Australia/Adelaide",
  "Australia/Brisbane",
  "Australia/Broken_Hill",
  "Australia/Canberra",
  "Australia/Currie",
  "Australia/Darwin",
  "Australia/Eucla",
  "Australia/Hobart",
  "Australia/LHI",
  "Australia/Lindeman",
  "Australia/Lord_Howe",
  "Australia/Melbourne",
  "Australia/NSW",
  "Australia/North",
  "Australia/Perth",
  "Australia/Queensland",
  "Australia/South",
  "Australia/Sydney",
  "Australia/Tasmania",
  "Australia/Victoria",
  "Australia/West",
  "Australia/Yancowinna",
  "Brazil/Acre",
  "Brazil/DeNoronha",
  "Brazil/East",
  "Brazil/West",
  "Canada/Atlantic",
  "Canada/Central",
  "Canada/East-Saskatchewan",
  "Canada/Eastern",
  "Canada/Mountain",
  "Canada/Newfoundland",
  "Canada/Pacific",
  "Canada/Saskatchewan",
  "Canada/Yukon",
  "Chile/Continental",
  "Chile/EasterIsland",
  "Europe/Amsterdam",
  "Europe/Andorra",
  "Europe/Athens",
  "Europe/Belfast",
  "Europe/Belgrade",
  "Europe/Berlin",
  "Europe/Bratislava",
  "Europe/Brussels",
  "Europe/Bucharest",
  "Europe/Budapest",
  "Europe/Busingen",
  "Europe/Chisinau",
  "Europe/Copenhagen",
  "Europe/Dublin",
  "Europe/Gibraltar",
  "Europe/Guernsey",
  "Europe/Helsinki",
  "Europe/Isle_of_Man",
  "Europe/Istanbul",
  "Europe/Jersey",
  "Europe/Kaliningrad",
  "Europe/Kiev",
  "Europe/Lisbon",
  "Europe/Ljubljana",
  "Europe/London",
  "Europe/Luxembourg",
  "Europe/Madrid",
  "Europe/Malta",
  "Europe/Mariehamn",
  "Europe/Minsk",
  "Europe/Monaco",
  "Europe/Moscow",
  "Europe/Nicosia",
  "Europe/Oslo",
  "Europe/Paris",
  "Europe/Podgorica",
  "Europe/Prague",
  "Europe/Riga",
  "Europe/Rome",
  "Europe/Samara",
  "Europe/San_Marino",
  "Europe/Sarajevo",
  "Europe/Simferopol",
  "Europe/Skopje",
  "Europe/Sofia",
  "Europe/Stockholm",
  "Europe/Tallinn",
  "Europe/Tirane",
  "Europe/Tiraspol",
  "Europe/Uzhgorod",
  "Europe/Vaduz",
  "Europe/Vatican",
  "Europe/Vienna",
  "Europe/Vilnius",
  "Europe/Volgograd",
  "Europe/Warsaw",
  "Europe/Zagreb",
  "Europe/Zaporozhye",
  "Europe/Zurich",
  "Indian/Antananarivo",
  "Indian/Chagos",
  "Indian/Christmas",
  "Indian/Cocos",
  "Indian/Comoro",
  "Indian/Kerguelen",
  "Indian/Mahe",
  "Indian/Maldives",
  "Indian/Mauritius",
  "Indian/Mayotte",
  "Indian/Reunion",
  "Mexico/BajaNorte",
  "Mexico/BajaSur",
  "Mexico/General",
  "Pacific/Apia",
  "Pacific/Auckland",
  "Pacific/Chatham",
  "Pacific/Chuuk",
  "Pacific/Easter",
  "Pacific/Efate",
  "Pacific/Enderbury",
  "Pacific/Fakaofo",
  "Pacific/Fiji",
  "Pacific/Funafuti",
  "Pacific/Galapagos",
  "Pacific/Gambier",
  "Pacific/Guadalcanal",
  "Pacific/Guam",
  "Pacific/Honolulu",
  "Pacific/Johnston",
  "Pacific/Kiritimati",
  "Pacific/Kosrae",
  "Pacific/Kwajalein",
  "Pacific/Majuro",
  "Pacific/Marquesas",
  "Pacific/Midway",
  "Pacific/Nauru",
  "Pacific/Niue",
  "Pacific/Norfolk",
  "Pacific/Noumea",
  "Pacific/Pago_Pago",
  "Pacific/Palau",
  "Pacific/Pitcairn",
  "Pacific/Pohnpei",
  "Pacific/Ponape",
  "Pacific/Port_Moresby",
  "Pacific/Rarotonga",
  "Pacific/Saipan",
  "Pacific/Samoa",
  "Pacific/Tahiti",
  "Pacific/Tarawa",
  "Pacific/Tongatapu",
  "Pacific/Truk",
  "Pacific/Wake",
  "Pacific/Wallis",
  "Pacific/Yap"
]

// Nodes
const country = document.querySelector("#country")
const country_code = document.querySelector("#country-code")
const time_zone = document.querySelector("#time-zone")
const phone = document.querySelector("#phone")
const full_number = document.querySelector("#full-phone")

// Set country options when the page loads
const options_countries = countries_codes.map(([country, code]) => `<option value="${country}">${country}</option>`)
country.innerHTML = options_countries
document.querySelector("#country option[value='México']").selected = true

// Update time zome when the page loads
const options_time_zones = time_zones.map(tz => `<option value="${tz}">${tz}</option>`)
time_zone.innerHTML = options_time_zones
document.querySelector("#time-zone option[value='America/Mexico_City']").selected = true

// Update country code when the country changes
document.querySelector("#country").addEventListener("change", e => {
  const code = countries_codes.find(c => c[0] === e.target.value)[1]
  document.querySelector("#country-code").innerHTML = "+" + code
})

// Update full number when the country code or number changes
function update_full_number () {
  const code = country_code.innerHTML
  const phone_number = phone.value
  full_number.value = `${code} ${phone_number}`
}
country.addEventListener("change", update_full_number)
phone.addEventListener("change", update_full_number)