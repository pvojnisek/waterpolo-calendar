# Calendar generator for waterpolo competitions

This utility generates calendars (ics files) from waterpolo competitions from the [MVLSZ - Hungarian Waterpolo Associations](https://waterpolo.hu) website.

## Sample calendars:

Production:
 - https://waterpolo-calendar.vercel.app/waterpolo/680/KSI?nocache   #gyerek orsz.
 - https://waterpolo-calendar.vercel.app/waterpolo/704/KSI?nocache   #gyerek BP
 - https://waterpolo-calendar.vercel.app/waterpolo/703/KSI?nocache   #serdülő BP
 

Preview: 
 - https://calendar-pvojnisek.vercel.app/waterpolo/680/KSI?nocache
 - https://calendar-pvojnisek.vercel.app/waterpolo/704/KSI?nocache

# Dev env

Starting environments:

 - backend: in the 'be/src/' directory: ```uvicorn index:app --reload```
 - frontend: in the 'fe/' directory: ```./start-dev.sh```
