from utils.actions.instagram import (
    first_action as IGselect_owner,
    second_action as IGentername1,
    third_action as IGemail,
    fourth as IGemail2,
    fifth as IGselectcountry,
    sixth as IGcopiedtype,
    seventh as IGentername2,
    eights as IGcopiedurl,
    nineth as IGcopieddesc,
    tenths as IGtargettype,
    elevenths as IGtargeturl,
    twelth as IGtargetdesc,
    thirtheenth as IGentername3,
    first_submit as IGsubmit1,
    fourteenth as IGotp,
    fifteenth as IGsubmit2,
    resendotp as IGresendotp,
)
from utils.actions.facebook import (
    first_action as FBselect_owner,
    second_action as FBentername1,
    third_action as FBemail,
    fourth as FBemail2,
    fifth as FBselectcountry,
    sixth as FBcopiedtype,
    seventh as FBentername2,
    eights as FBcopiedurl,
    nineth as FBcopieddesc,
    tenths as FBtargettype,
    elevenths as FBtargeturl,
    twelth as FBtargetdesc,
    thirtheenth as FBentername3,
    first_submit as FBsubmit1,
    fourteenth as FBotp,
    fifteenth as FBsubmit2,
    resendotp as IGresendotp,
)


PLATFORMS = {
    "instagram": {
        "url": "https://help.instagram.com/contact/552695131608132",
        "actions": {
            "owner": IGselect_owner,
            "name1": IGentername1,
            "email1": IGemail,
            "email2": IGemail2,
            "country": IGselectcountry,
            "copiedtype": IGcopiedtype,
            "name2": IGentername2,
            "copiedurl": IGcopiedurl,
            "copieddesc": IGcopieddesc,
            "targettype": IGtargettype,
            "targeturl": IGtargeturl,
            "targetdesc": IGtargetdesc,
            "name3": IGentername3,
            "submit1": IGsubmit1,
            "otp": IGotp,
            "submit2": IGsubmit2,
            "resendotp": IGresendotp,
        }
    },
    "facebook": {
        "url": "https://www.facebook.com/help/contact/copyrightform",
        "actions": {
            "owner": FBselect_owner,
            "name1": FBentername1,
            "email1": FBemail,
            "email2": FBemail2,
            "country": FBselectcountry,
            "copiedtype": FBcopiedtype,
            "name2": FBentername2,
            "copiedurl": FBcopiedurl,
            "copieddesc": FBcopieddesc,
            "targettype": FBtargettype,
            "targeturl": FBtargeturl,
            "targetdesc": FBtargetdesc,
            "name3": FBentername3,
            "submit1": FBsubmit1,
            "otp": FBotp,
            "submit2": FBsubmit2,
            "resendotp": IGresendotp,
        }
    }
}

def get_platform_config(platform: str):
    cfg = PLATFORMS.get(platform.lower())
    if not cfg:
        raise ValueError(f"Unsupported platform: {platform}. Supported: {list(PLATFORMS.keys())}")
    return cfg