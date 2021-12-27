# Create your views here.

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

import re

MAX_LEVEL = 99.0;
MAX_STAT = 255.0;
MAX_HP = 9999.0;
MAX_MP = 999.0;

MAX_EVADE = 90.0;
MIN_EVADE = 5.0;

MAX_CRIT = 90.0
MIN_CRIT = 5.0;

BASE_AFFINITY = 100.0;

BaseCrit = int(MAX_STAT / MAX_CRIT * MIN_CRIT + .0001);


def index(request):
	return render_to_response('bqsite/home.html')

def changelog(request):
	return render_to_response('bqsite/changelog.html')




def charsim(request):
    return render_to_response('bqsite/charsim.html')

@csrf_exempt
def csUpdate(request):
    if request.is_ajax():
        inData = lambda name: getFormData(request, name)

	level = int(inData('charLevel'));
        
        
        data = {}
        data['charIndex'] = inData('charIndex');
        
        #Primaries
        buildPrimaryStat(data, request, level, "Strength");
        buildPrimaryStat(data, request, level, "Agility");
        buildPrimaryStat(data, request, level, "Vitality");
        buildPrimaryStat(data, request, level, "Intelligence");
        
        #Secondaries:
        data['baseHP'] = calcHPMPValue(data['baseVitality'], level, MAX_HP);
        data['finalHP'] = max(1.0, min(MAX_HP, data['baseHP'] + int(inData('bonusHP'))));
        data['baseMP'] = calcHPMPValue(data['baseIntelligence'], level, MAX_MP);
        data['finalMP'] = max(1.0, min(MAX_MP, data['baseMP'] + int(inData('bonusMP'))));
        
        data['basePower'] = max(0, data['finalStrength'] + int(inData('Weapon')));       
        data['finalPower'] = max(0, data['basePower'] + int(inData('bonusPower')));
        data['baseDefense'] = max(0, min(MAX_STAT, int(inData('Armor'))));       
        data['finalDefense'] = max(0, min(MAX_STAT, data['baseDefense'] + int(inData('bonusDefense'))));
        
        data['baseMagicPower'] = max(0, min(MAX_STAT, data['finalIntelligence']));       
        data['finalMagicPower'] = max(0, min(MAX_STAT, data['baseMagicPower'] + int(inData('bonusMagicPower'))));
        
        data['baseMagicDefense'] = max(0, min(MAX_STAT, data['finalIntelligence']));       
        data['finalMagicDefense'] = max(0, min(MAX_STAT, data['baseMagicDefense'] + int(request.POST['bonusMagicDefense'])));
        
        data['baseSpeed'] = max(0, min(MAX_STAT, data['finalAgility']));       
        data['finalSpeed'] = max(0, min(MAX_STAT, data['baseSpeed'] + int(inData('bonusSpeed'))));
        
        data['baseEvade'] = max(0, min(MAX_STAT, calcEvade(level, data['finalAgility'])));   
        data['finalEvade'] = max(0, min(MAX_STAT, data['baseEvade'] + int(inData('bonusEvade'))));
        
        data['finalBlock'] = max(0, min(MAX_STAT, int(inData('bonusBlock'))));
        data['finalNullify'] = max(0, min(MAX_STAT, int(inData('bonusNullify'))));
        
        data['baseFerocity'] = BaseCrit;
        data['finalFerocity'] = max(0, min(MAX_STAT, data['baseFerocity'] + int(inData('bonusFerocity'))));
        
        
        
        
        data['baseFire'] = BASE_AFFINITY;
        data['baseEarth'] = BASE_AFFINITY;
        data['baseWind'] = BASE_AFFINITY;
        data['baseWater'] = BASE_AFFINITY;
        data['finalFire'] = max(0, min(MAX_STAT, data['baseFire'] + int(inData('bonusFire'))));
        data['finalEarth'] = max(0, min(MAX_STAT, data['baseEarth'] + int(inData('bonusEarth'))));
        data['finalWind'] = max(0, min(MAX_STAT, data['baseWind'] + int(inData('bonusWind'))));
        data['finalWater'] = max(0, min(MAX_STAT, data['baseWater'] + int(inData('bonusWater'))));
        
        
        physical = request.POST['damageType'] == 'p';
        guarding = request.POST['guarding'].lower() == 'true'
        ignoreDef = request.POST['ignoreDef'].lower() == 'true'
        
        AP = data['finalPower'] if physical else data['finalMagicPower']
        DP = int(inData('dfinalDefense')) if physical else int(inData('dfinalMagicDefense'))
        if ignoreDef: DP = 0.0
       
        dmg = AP * 10.0
        reduceFactor = pow(DP/MAX_STAT, 0.7)
        moddedDmg = dmg * (1.0 - reduceFactor) * inData('attackPower');

        data['outBaseDamage'] = "%.2f"%(moddedDmg);

        
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    
    return render_to_response('bqsite/charsim.html')

@csrf_exempt
def csAddChar(request):
    if request.is_ajax():
        charIndex = request.POST['charIndex']
        html = render_to_string("bqsite/charbox.html", {"charIndex":charIndex})
        htmlrow = render_to_string("bqsite/charRow.html", {"charIndex":"row"+charIndex})
        
        serialized_data = simplejson.dumps({"charIndex":charIndex, "html":html, "htmlrow":htmlrow})
        return HttpResponse(serialized_data, mimetype="application/json")
    
    return render_to_response('bqsite/charsim.html')

def getFormData(request, name):
    try:
        return float(request.POST[name])
    except ValueError:
        return 0


def buildPrimaryStat(data, request, level, statName):
    data['base'+statName] = max(0, min(MAX_STAT, int(getFormData(request, 'rating'+statName)*25.5)));
    data['current'+statName] = max(0, min(MAX_STAT, int(data['base'+statName] * (level / MAX_LEVEL ))));
    data['final'+statName] = max(0, min(MAX_STAT, data['current'+statName] + int(getFormData(request, 'bonus'+statName))));    
    
    
def calcHPMPValue(finalStat, level, maxi):
    invLevel = level / MAX_LEVEL
    curve = 0.3 + (invLevel * 0.7)
    invFinalStat = finalStat / MAX_STAT
    
    ret = curve*invLevel*(maxi*invFinalStat*0.2+ 
          maxi*0.8+invLevel*0.4*maxi*invFinalStat
          -invLevel*0.4*maxi);
          
    ret += .0001;
          
    return int(max(1.0, min(maxi, ret)));

def calcEvade(level, agility):
    pointsPerPercent = 255.0 / MAX_EVADE;
    levelBonus = int(pointsPerPercent * 10.0 / 99.0 * level + .0001);
    agiBonus = int(pointsPerPercent * 10.0 / 255.0 * agility + .0001);
    minBonus = int(pointsPerPercent * MIN_EVADE + .0001);
    
    return minBonus + levelBonus + agiBonus;
