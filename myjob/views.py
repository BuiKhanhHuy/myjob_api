import json
import random
import requests
from django.db import transaction
from console.jobs import queue_notification, queue_job
from infobip_channels.sms.channel import SMSChannel
from django.conf import settings
from helpers import helper, utils
from configs import renderers
from configs import variable_response as var_res, variable_system as var_sys
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions as perms_sys
from .models import (
    Feedback,
    Banner
)
from authentication.models import (
    User
)
from common.models import (
    Location,
    District,
)
from info.models import (
    Company,
    JobSeekerProfile,
    Resume
)
from job.models import (
    JobPost
)
from .serializers import (
    FeedbackSerializer,
    BannerSerializer
)


@api_view(http_method_names=["POST"])
def create_fake_data(request):
    with open(settings.JSON_PATH + "data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    with transaction.atomic():
        i = 0
        company_name_list = []
        for index, d in enumerate(data):
            if utils.remove_accents(d.get("company")["company_name"].lower()) in company_name_list:
                print("trùng: ", d.get("company")["company_name"].lower())
                continue

            try:
                location_data = d.get("location")
                city_id = location_data["city_id"]
                if str(city_id) == str(54):
                    continue
                districts_id = District.objects.filter(city_id=city_id).values_list("id", flat=True)
                location_data["district_id"] = random.choice(districts_id)
            except:
                continue

            tax_code = f"0888{100000 + i}"
            user_data = d.get("user")

            company_data = d.get("company")
            company_data["tax_code"] = tax_code

            jobs_post_data = d.get("jobs")
            # create user
            user = User.objects.create(**user_data)
            user.set_password(user.password)
            user.save()
            # create company location
            company_location = Location.objects.create(**location_data)
            # create company
            company = Company.objects.create(**company_data, user=user, location=company_location)

            # create job posts of company
            for job in jobs_post_data:
                job_post_location = Location.objects.create(**location_data)
                JobPost.objects.create(**job, user=user, company=company, location=job_post_location)

            i = i + 1
            company_name_list.append(utils.remove_accents(d.get("company")["company_name"].lower()))

    return var_res.response_data(data={
        "LIST_NAME": company_name_list,
    })


@api_view(http_method_names=['POST'])
def get_job_seeker_data_fake(request):
    map_data = {
        "career_map": {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "11": 11,
            "12": 12,
            "13": 13,
            "14": 14,
            "15": 15,
            "16": 16,
            "17": 17,
            "18": 18,
            "19": 19,
            "20": 20,
            "21": 21,
            "22": 22,
            "23": 23,
            "24": 24,
            "25": 25,
            "26": 26,
            "27": 27,
            "28": 28,
            "29": 29,
            "30": 30,
            "31": 31,
            "32": 32,
            "33": 33,
            "34": 34,
            "35": 35
        },
        "tinh_map": {
            "73": 1,
            "122": 2,
            "129": 3,
            "121": 4,
            "76": 5,
            "87": 6,
            "134": 7,
            "90": 8,
            "125": 9,
            "119": 10,
            "117": 11,
            "111": 12,
            "107": 13,
            "135": 14,
            "131": 15,
            "75": 16,
            "113": 17,
            "74": 18,
            "95": 19,
            "100": 20,
            "91": 21,
            "92": 22,
            "132": 23,
            "83": 24,
            "93": 25,
            "109": 26,
            "130": 27,
            "112": 28,
            "80": 29,
            "116": 30,
            "85": 31,
            "78": 32,
            "123": 33,
            "96": 34,
            "99": 35,
            "97": 36,
            "110": 37,
            "140": 38,
            "88": 39,
            "108": 40,
            "101": 41,
            "105": 42,
            "106": 43,
            "86": 44,
            "102": 45,
            "133": 46,
            "81": 47,
            "118": 48,
            "94": 49,
            "84": 50,
            "98": 51,
            "103": 52,
            "124": 53,
            "136": 54,
            "126": 55,
            "77": 56,
            "127": 57,
            "89": 58,
            "82": 59,
            "104": 60,
            "114": 61,
            "115": 62,
            "79": 63,
            "120": 64,
            "128": 65
        },
        "huyen_map": {
            "232": 1,
            "233": 2,
            "234": 3,
            "235": 4,
            "236": 5,
            "237": 6,
            "238": 7,
            "239": 8,
            "240": 9,
            "241": 10,
            "242": 11,
            "243": 12,
            "244": 13,
            "245": 14,
            "246": 15,
            "247": 16,
            "248": 17,
            "249": 18,
            "250": 19,
            "251": 20,
            "252": 21,
            "253": 22,
            "254": 23,
            "255": 24,
            "256": 25,
            "257": 26,
            "258": 27,
            "259": 28,
            "260": 29,
            "261": 30,
            "308": 31,
            "309": 32,
            "310": 33,
            "312": 34,
            "313": 35,
            "314": 36,
            "315": 37,
            "316": 38,
            "318": 39,
            "319": 40,
            "320": 41,
            "321": 42,
            "322": 43,
            "323": 44,
            "324": 45,
            "325": 46,
            "326": 47,
            "327": 48,
            "328": 49,
            "329": 50,
            "330": 51,
            "331": 52,
            "1": 53,
            "2": 54,
            "3": 55,
            "4": 56,
            "5": 57,
            "6": 58,
            "7": 59,
            "8": 60,
            "9": 61,
            "10": 62,
            "11": 63,
            "12": 64,
            "13": 65,
            "14": 66,
            "15": 67,
            "16": 68,
            "17": 69,
            "18": 70,
            "19": 71,
            "30": 72,
            "31": 73,
            "32": 74,
            "33": 75,
            "34": 76,
            "35": 77,
            "36": 78,
            "37": 79,
            "20": 80,
            "21": 81,
            "22": 82,
            "23": 83,
            "24": 84,
            "25": 85,
            "26": 86,
            "27": 87,
            "28": 88,
            "29": 89,
            "38": 90,
            "39": 91,
            "40": 92,
            "41": 93,
            "42": 94,
            "43": 95,
            "44": 96,
            "45": 97,
            "46": 98,
            "47": 99,
            "48": 100,
            "49": 101,
            "50": 102,
            "51": 103,
            "52": 104,
            "53": 105,
            "54": 106,
            "55": 107,
            "56": 108,
            "57": 109,
            "58": 110,
            "59": 111,
            "60": 112,
            "72": 113,
            "73": 114,
            "74": 115,
            "75": 116,
            "76": 117,
            "77": 118,
            "78": 119,
            "79": 120,
            "80": 121,
            "81": 122,
            "82": 123,
            "83": 124,
            "84": 125,
            "85": 126,
            "86": 127,
            "87": 128,
            "88": 129,
            "89": 130,
            "90": 131,
            "91": 132,
            "92": 133,
            "93": 134,
            "94": 135,
            "95": 136,
            "96": 137,
            "97": 138,
            "98": 139,
            "61": 140,
            "62": 141,
            "63": 142,
            "64": 143,
            "65": 144,
            "66": 145,
            "67": 146,
            "68": 147,
            "69": 148,
            "70": 149,
            "71": 150,
            "99": 151,
            "100": 152,
            "101": 153,
            "102": 154,
            "103": 155,
            "104": 156,
            "105": 157,
            "106": 158,
            "107": 159,
            "108": 160,
            "109": 161,
            "110": 162,
            "111": 163,
            "112": 164,
            "113": 165,
            "114": 166,
            "115": 167,
            "116": 168,
            "117": 169,
            "118": 170,
            "119": 171,
            "120": 172,
            "121": 173,
            "122": 174,
            "123": 175,
            "124": 176,
            "125": 177,
            "126": 178,
            "127": 179,
            "128": 180,
            "129": 181,
            "198": 182,
            "199": 183,
            "200": 184,
            "201": 185,
            "202": 186,
            "203": 187,
            "204": 188,
            "205": 189,
            "206": 190,
            "207": 191,
            "208": 192,
            "209": 193,
            "210": 194,
            "211": 195,
            "212": 196,
            "213": 197,
            "214": 198,
            "215": 199,
            "216": 200,
            "217": 201,
            "218": 202,
            "219": 203,
            "220": 204,
            "221": 205,
            "222": 206,
            "223": 207,
            "224": 208,
            "225": 209,
            "226": 210,
            "227": 211,
            "228": 212,
            "229": 213,
            "230": 214,
            "231": 215,
            "262": 216,
            "263": 217,
            "264": 218,
            "265": 219,
            "266": 220,
            "267": 221,
            "268": 222,
            "269": 223,
            "270": 224,
            "271": 225,
            "272": 226,
            "273": 227,
            "274": 228,
            "275": 229,
            "276": 230,
            "277": 231,
            "278": 232,
            "279": 233,
            "280": 234,
            "281": 235,
            "282": 236,
            "283": 237,
            "284": 238,
            "285": 239,
            "286": 240,
            "287": 241,
            "288": 242,
            "289": 243,
            "290": 244,
            "291": 245,
            "292": 246,
            "293": 247,
            "294": 248,
            "295": 249,
            "296": 250,
            "297": 251,
            "298": 252,
            "299": 253,
            "300": 254,
            "301": 255,
            "302": 256,
            "303": 257,
            "304": 258,
            "305": 259,
            "306": 260,
            "307": 261,
            "332": 262,
            "333": 263,
            "334": 264,
            "335": 265,
            "336": 266,
            "337": 267,
            "338": 268,
            "339": 269,
            "340": 270,
            "341": 271,
            "342": 272,
            "343": 273,
            "344": 274,
            "345": 275,
            "346": 276,
            "347": 277,
            "348": 278,
            "349": 279,
            "350": 280,
            "351": 281,
            "352": 282,
            "353": 283,
            "354": 284,
            "355": 285,
            "356": 286,
            "357": 287,
            "358": 288,
            "359": 289,
            "360": 290,
            "361": 291,
            "362": 292,
            "363": 293,
            "364": 294,
            "365": 295,
            "366": 296,
            "367": 297,
            "368": 298,
            "369": 299,
            "370": 300,
            "371": 301,
            "372": 302,
            "373": 303,
            "374": 304,
            "375": 305,
            "376": 306,
            "377": 307,
            "378": 308,
            "379": 309,
            "380": 310,
            "381": 311,
            "382": 312,
            "383": 313,
            "384": 314,
            "385": 315,
            "386": 316,
            "387": 317,
            "388": 318,
            "389": 319,
            "390": 320,
            "391": 321,
            "392": 322,
            "393": 323,
            "394": 324,
            "395": 325,
            "396": 326,
            "397": 327,
            "398": 328,
            "399": 329,
            "400": 330,
            "401": 331,
            "402": 332,
            "403": 333,
            "404": 334,
            "405": 335,
            "406": 336,
            "407": 337,
            "408": 338,
            "409": 339,
            "410": 340,
            "411": 341,
            "412": 342,
            "413": 343,
            "414": 344,
            "415": 345,
            "416": 346,
            "417": 347,
            "418": 348,
            "419": 349,
            "420": 350,
            "421": 351,
            "422": 352,
            "423": 353,
            "424": 354,
            "425": 355,
            "426": 356,
            "427": 357,
            "428": 358,
            "429": 359,
            "430": 360,
            "431": 361,
            "432": 362,
            "433": 363,
            "434": 364,
            "435": 365,
            "436": 366,
            "437": 367,
            "438": 368,
            "439": 369,
            "440": 370,
            "441": 371,
            "442": 372,
            "443": 373,
            "444": 374,
            "445": 375,
            "446": 376,
            "447": 377,
            "448": 378,
            "449": 379,
            "450": 380,
            "451": 381,
            "452": 382,
            "453": 383,
            "454": 384,
            "455": 385,
            "456": 386,
            "457": 387,
            "458": 388,
            "459": 389,
            "460": 390,
            "461": 391,
            "462": 392,
            "463": 393,
            "464": 394,
            "465": 395,
            "466": 396,
            "467": 397,
            "468": 398,
            "469": 399,
            "470": 400,
            "471": 401,
            "472": 402,
            "473": 403,
            "474": 404,
            "475": 405,
            "476": 406,
            "477": 407,
            "478": 408,
            "479": 409,
            "480": 410,
            "481": 411,
            "482": 412,
            "483": 413,
            "484": 414,
            "485": 415,
            "486": 416,
            "487": 417,
            "488": 418,
            "489": 419,
            "490": 420,
            "491": 421,
            "492": 422,
            "493": 423,
            "494": 424,
            "495": 425,
            "496": 426,
            "497": 427,
            "498": 428,
            "499": 429,
            "500": 430,
            "501": 431,
            "502": 432,
            "503": 433,
            "504": 434,
            "505": 435,
            "506": 436,
            "507": 437,
            "508": 438,
            "509": 439,
            "510": 440,
            "511": 441,
            "512": 442,
            "513": 443,
            "514": 444,
            "515": 445,
            "516": 446,
            "517": 447,
            "518": 448,
            "519": 449,
            "520": 450,
            "521": 451,
            "522": 452,
            "523": 453,
            "524": 454,
            "525": 455,
            "526": 456,
            "527": 457,
            "528": 458,
            "529": 459,
            "530": 460,
            "531": 461,
            "532": 462,
            "533": 463,
            "534": 464,
            "535": 465,
            "536": 466,
            "537": 467,
            "538": 468,
            "539": 469,
            "540": 470,
            "541": 471,
            "542": 472,
            "543": 473,
            "544": 474,
            "545": 475,
            "546": 476,
            "547": 477,
            "548": 478,
            "549": 479,
            "550": 480,
            "551": 481,
            "552": 482,
            "553": 483,
            "554": 484,
            "555": 485,
            "556": 486,
            "557": 487,
            "558": 488,
            "559": 489,
            "560": 490,
            "561": 491,
            "562": 492,
            "563": 493,
            "564": 494,
            "565": 495,
            "566": 496,
            "567": 497,
            "568": 498,
            "569": 499,
            "570": 500,
            "571": 501,
            "572": 502,
            "573": 503,
            "574": 504,
            "575": 505,
            "576": 506,
            "577": 507,
            "578": 508,
            "579": 509,
            "580": 510,
            "581": 511,
            "582": 512,
            "583": 513,
            "584": 514,
            "585": 515,
            "586": 516,
            "587": 517,
            "588": 518,
            "589": 519,
            "590": 520,
            "591": 521,
            "592": 522,
            "593": 523,
            "594": 524,
            "595": 525,
            "596": 526,
            "597": 527,
            "598": 528,
            "599": 529,
            "600": 530,
            "601": 531,
            "602": 532,
            "603": 533,
            "604": 534,
            "605": 535,
            "606": 536,
            "607": 537,
            "608": 538,
            "609": 539,
            "610": 540,
            "611": 541,
            "612": 542,
            "613": 543,
            "614": 544,
            "615": 545,
            "616": 546,
            "617": 547,
            "618": 548,
            "619": 549,
            "620": 550,
            "621": 551,
            "622": 552,
            "623": 553,
            "624": 554,
            "625": 555,
            "626": 556,
            "627": 557,
            "628": 558,
            "629": 559,
            "630": 560,
            "631": 561,
            "632": 562,
            "633": 563,
            "634": 564,
            "635": 565,
            "636": 566,
            "637": 567,
            "638": 568,
            "639": 569,
            "640": 570,
            "641": 571,
            "642": 572,
            "643": 573,
            "644": 574,
            "645": 575,
            "646": 576,
            "647": 577,
            "648": 578,
            "649": 579,
            "650": 580,
            "651": 581,
            "652": 582,
            "653": 583,
            "654": 584,
            "655": 585,
            "656": 586,
            "657": 587,
            "658": 588,
            "659": 589,
            "660": 590,
            "661": 591,
            "662": 592,
            "663": 593,
            "664": 594,
            "665": 595,
            "666": 596,
            "667": 597,
            "668": 598,
            "669": 599,
            "670": 600,
            "671": 601,
            "672": 602,
            "673": 603,
            "674": 604,
            "675": 605,
            "676": 606,
            "677": 607,
            "678": 608,
            "679": 609,
            "680": 610,
            "681": 611,
            "682": 612,
            "683": 613,
            "684": 614,
            "685": 615,
            "686": 616,
            "687": 617,
            "688": 618,
            "689": 619,
            "690": 620,
            "691": 621,
            "692": 622,
            "693": 623,
            "694": 624,
            "695": 625,
            "696": 626,
            "697": 627,
            "698": 628,
            "699": 629,
            "700": 630,
            "701": 631,
            "702": 632,
            "703": 633,
            "704": 634,
            "705": 635,
            "130": 636,
            "131": 637,
            "132": 638,
            "133": 639,
            "134": 640,
            "135": 641,
            "136": 642,
            "137": 643,
            "138": 644,
            "139": 645,
            "140": 646,
            "141": 647,
            "142": 648,
            "143": 649,
            "144": 650,
            "145": 651,
            "146": 652,
            "147": 653,
            "148": 654,
            "149": 655,
            "150": 656,
            "151": 657,
            "152": 658,
            "153": 659,
            "154": 660,
            "155": 661,
            "156": 662,
            "165": 663,
            "157": 664,
            "158": 665,
            "159": 666,
            "160": 667,
            "161": 668,
            "162": 669,
            "163": 670,
            "164": 671,
            "166": 672,
            "167": 673,
            "168": 674,
            "169": 675,
            "170": 676,
            "171": 677,
            "172": 678,
            "173": 679,
            "174": 680,
            "175": 681,
            "176": 682,
            "177": 683,
            "178": 684,
            "179": 685,
            "180": 686,
            "181": 687,
            "182": 688,
            "183": 689,
            "184": 690,
            "185": 691,
            "186": 692,
            "187": 693,
            "188": 694,
            "189": 695,
            "190": 696,
            "191": 697,
            "192": 698,
            "193": 699,
            "194": 700,
            "195": 701,
            "196": 702,
            "197": 703
        },
        "gender_map": {
            "1": "O",
            "2": "M",
            "3": "F"
        }
    }

    url = "https://apiv2.vieclam24h.vn/seeker/fe/search/resume?updated_at=&action=search&includes=is_seen&"
    authorization = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFubmVsX2NvZGUiOiJ2bDI0aCIsInVzZXIiOnsiaWQiOiIxMDAxMDc3ODgiLCJlbWFpbCI6IjE5NTEwNTAwMjdodXlAb3UuZWR1LnZuIiwibmFtZSI6IkFhIiwiYXZhdGFyIjpudWxsLCJoYXNfcGFzcyI6IjRhZTYzZTRjMjZmNWQ1ZDAyZmYxMjZlNTJiYjA5ZDQzIiwicm9sZSI6ImVtcGxveWVyIn0sImV4cCI6MTcxNDY3MzU1MH0.7pWVd1jS7YV0FIf-KL7wsIcod5ktFwqVD-j9P12B8Mc"
    i = 1500
    page = 15

    while page < 1390:
        response = requests.get(url + f"per_page=100&page={page}", headers={
            "Authorization": authorization
        })
        items = json.loads(response.text).get("data").get("items")
        with transaction.atomic():
            for idx, item in enumerate(items):
                user_data = {
                    "password": "123",
                    "full_name": item.get("seeker_info").get("name"),
                    "email": f'{utils.remove_accents(item.get("seeker_info").get("name")).replace(" ", "").lower()}{i}@gmail.com',
                    "has_company": 0,
                    "is_active": True,
                    "is_verify_email": True,
                    "role_name": "JOB_SEEKER"
                }
                job_seeker_profile_data = {
                    "phone": f"08{10000000 + i}",
                    "birthday": item.get("seeker_info").get("birthday"),
                    "marital_status": "S",
                }

                # chi tiet
                idd = item.get("id")
                url1 = "https://apiv2.vieclam24h.vn/seeker/fe/resume/"
                response1 = requests.get(url1 + f"{idd}?id={idd}", headers={
                    "Authorization": authorization
                })

                seeker_data = json.loads(response1.text).get("data")
                resume_data = {
                    "title": seeker_data.get("title"),
                    "description": seeker_data.get("career_objective"),
                    "salary_min": seeker_data.get("min_expected_salary"),
                    "salary_max": seeker_data.get("min_expected_salary") + 5000000,
                    "position": random.randint(1, 9),
                    "experience": random.randint(1, 8),
                    "academic_level": random.randint(1, 6),
                    "type_of_workplace": random.randint(1, 3),
                    "job_type": random.randint(1, 4),
                    "is_active": 1,
                    "type": "WEBSITE",
                    "career_id": map_data["career_map"].get(str(seeker_data.get("occupation_ids")[0])),
                    "city_id": map_data["tinh_map"].get(str(seeker_data.get("province_ids")[0])),
                }
                user = User.objects.create(**user_data)
                user.set_password(user.password)
                user.save()

                job_seeker_profile = JobSeekerProfile.objects.create(**job_seeker_profile_data, user=user)

                Resume.objects.create(**resume_data, user=user, job_seeker_profile=job_seeker_profile)

                i += 1
                print(f"=> Page: {page} =>  Xong em {idx + 1}")
        page = page + 5
    return var_res.response_data(data="OKE")


class FeedbackViewSet(viewsets.ViewSet,
                      generics.CreateAPIView,
                      generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    renderer_classes = [renderers.MyJSONRenderer]

    def get_permissions(self):
        if self.action in ["create"]:
            return [perms_sys.IsAuthenticated()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(is_active=True).order_by('-rating')[:10])

        serializer = self.get_serializer(queryset, many=True,
                                         fields=['id', 'content', 'rating', 'isActive', 'userDict'])
        return var_res.Response(serializer.data)


@api_view(http_method_names=['post'])
def send_sms_download_app(request):
    data = request.data
    if "phone" not in data:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors={"phone": ["Số điện thoại là bắt buộc."]})
    phone = data.get("phone")
    if not phone:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors={"phone": ["Số điện thoại không hợp lệ."]})
    try:
        # Initialize the SMS channel with your credentials.
        channel = SMSChannel.from_auth_params(
            {
                "base_url": settings.SMS_BASE_URL,
                "api_key": settings.SMS_API_KEY,
            }
        )
        # Send a message with the desired fields.
        sms_response = channel.send_sms_message(
            {
                "messages": [
                    {
                        "destinations": [{"to": phone}],
                        "text": f'Tin nhắn được gửi từ {settings.COMPANY_NAME}, '
                                f'Ứng dụng và Website giới thiệu việc làm. '
                                f'Với {settings.COMPANY_NAME}, '
                                f'bạn có thể tìm kiếm các công việc phù hợp với nhu cầu '
                                f'và kinh nghiệm của mình chỉ trong vài phút. '
                                f'Để tải ứng dụng, bạn có thể truy cập vào link sau: '
                                f'Android: {var_sys.LINK_GOOGLE_PLAY}; iOS: {var_sys.LINK_APPSTORE}. '
                                f'Hãy cùng trải nghiệm và tìm kiếm công '
                                f'việc mơ ước của bạn với {settings.COMPANY_NAME} nhé!'
                    }
                ]
            }
        )
        print(">> SMS SEND: ", sms_response)
    except Exception as ex:
        helper.print_log_error("send_sms_download_app", ex)
        var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return var_res.response_data()


@api_view(http_method_names=['get'])
def get_web_banner(request):
    banner_queryset = Banner.objects.filter(is_active=True, platform="WEB")
    serializer = BannerSerializer(banner_queryset, many=True, fields=[
        "id", "imageUrl", "buttonText", "description",
        "buttonLink", "isShowButton", "descriptionLocation"
    ])

    return var_res.response_data(data=serializer.data)


@api_view(http_method_names=['get'])
def get_mobile_banner(request):
    banner_type = request.GET.get("type", "HOME")
    if banner_type not in [x[1] for x in var_sys.BANNER_TYPE]:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST)
    banner_queryset = Banner.objects.filter(is_active=True, platform="APP")
    serializer = BannerSerializer(banner_queryset, many=True, fields=[
        "id", "imageMobileUrl", "buttonText", "description",
        "buttonLink", "isShowButton", "descriptionLocation"
    ])

    return var_res.response_data(data=serializer.data)


@api_view(http_method_names=['post'])
def send_notification_demo(request):
    data = request.data

    title = data.get("title", "TEST")
    content = data.get('content', "TEST CONTENT")
    user_list = data.get('userList', [])
    notification_type = data.get("type", "SYSTEM")
    body_content = data.get('bodyContent', {})
    image_link = data.get("imageLink", None)

    # queue_job.send_email_job_post_for_job_seeker_task.delay(1)
    queue_notification.add_notification_to_user.delay(
        title=title,
        content=content,
        type_name=notification_type,
        image=image_link,
        content_of_type=body_content,
        user_id_list=user_list
    )
    return var_res.response_data()
