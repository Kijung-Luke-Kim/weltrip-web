from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import Planner, Rating
from users.models import Profile

from search.search import *
from search.views import *
from .u_plans import *


# 테스트용함수 #
def viewplan(request):
    if 'id_userplan' in request.POST and request.POST['id_userplan']:
        user_input = request.POST['id_userplan']
        user_output = callPlans(user_input)
        return render(request, 'planner/viewplan.html', {'plan_list':user_output})

    elif 'pk_userplan' in request.POST and request.POST['pk_userplan']:
        pk_input = request.POST['pk_userplan']
        pk_output = callPlan(pk_input)

        # 객체 생성부
        plan_output = toPlan(pk_output.contents)
        plan_output.userId = pk_output.user
        
        return render(request, 'planner/viewplan.html', {'plan_slct':plan_output})


    else:
        return render(request, 'planner/viewplan.html')

# 테스트용 함수 #
def cplan(request):
    if 'search-key' in request.POST and request.POST['search-key']:
        siteKey = request.POST['search-key']
        print(siteKey)
        api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        results_tmp = searchByKeyword(siteKey, api_tmp)
        print(results_tmp)
        results_list = []
        for elm in results_tmp:
            elm_tmp = getInfos(elm)
            dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid')}
            results_list.append(dic_tmp)
        # output_list = checkInfos(result_list, 'title')
        
        print(results_list)
        return render(request, 'planner/cp_createplan.html', {'site_searched':results_list})
    if 'siteAdded' in request.POST and request.POST['siteAdded']:
        target_id = request.POST.get('siteAdded')
        target = Planner.objects.get(id=3)
        target.contents = target.contents + '{0}:60&'.format(target_id)
        target.save()
        return render(request, 'planner/cp_createplan.html')

    else:
        return render(request, 'planner/cp_createplan.html')




def index(request):
    return render(request, 'planner/index.html')

def plannerchoice(request):
    return render(request, 'planner/plannerchoice.html')

def createplan(request):
    if 'pk_del' in request.POST and request.POST['pk_del']:
        target_id = request.POST.get('pk_del')
        target = Planner.objects.get(id=target_id)
        target.delete()

        user_input = request.user
        user_output = callPlans(user_input)
        return render(request, 'planner/createplan.html', {'plan_list':user_output})

    if request.user or user:
        user_input = request.user
        user_output = callPlans(user_input)
    
        return render(request, 'planner/createplan.html', {'plan_list':user_output})

    else:
        return render(request, 'planner/createplan.html')

def directplan(request):
    if ('add_request_user' in request.POST and request.POST['add_request_user']) and ('contentId' in request.POST and request.POST['contentId']):
        user_input = request.POST.get('add_request_user')
        user_output = callPlans(user_input)
        add_cId = request.POST.get('contentId')
        add_cName = request.POST.get('contentName')
        return render(request, 'planner/createplan_direct.html', {'plan_list':user_output, 'add_cId':add_cId, 'add_cName':add_cName, 'add_user':user_input,})
        
    else:
        return render(request, 'planner/createplan_direct.html')
    

def makeplanid(request):

    if 'new_plan_title' in request.POST and request.POST:
        new_title = request.POST.get('new_plan_title')
        Planner(date = datetime.datetime.today(), user = request.user, title = new_title, contents='', rating=False).save()

        user_input = request.user
        user_output = callPlans(user_input)

        if request.POST.get('is_direct') == 'TRUE':
            add_cId = request.POST.get('contentId')
            add_cName = request.POST.get('contentName')
            add_user = request.POST.get('add_request_user')
            return render(request, 'planner/createplan_direct.html', {'plan_list':user_output, 'contentId':add_cId, 'contentName':add_cName, 'add_request_user':add_user,})

        return render(request, 'planner/createplan.html', {'plan_list':user_output})
    else:
        return render(request, 'planner/makeplanid.html')
   

def showplan(request):
    return render(request, 'planner/showplan.html')


def reviseplan(request):
    # 선택된 일정표 불러오기
    if 'pk_userplan' in request.POST and request.POST['pk_userplan']:
        pk_input = request.POST.get('pk_userplan')
        pk_output = callPlan(pk_input)

        # 객체 생성
        plan_output = toPlan(pk_output.contents)
        plan_output.userId = pk_output.user

        if 'siteAdded' in request.POST and request.POST['siteAdded']:
            target_id = request.POST.get('siteAdded')
            target = Planner.objects.get(id=pk_input)
            target.contents = target.contents + '{0}:60&'.format(target_id)
            target.save()

            pk_output = callPlan(pk_input)
            plan_output = toPlan(pk_output.contents)
            plan_output.userId = pk_output.user
            
            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

        if 'sitetoDel' in request.POST and request.POST['sitetoDel']:
            target_id = request.POST.get('sitetoDel')
            target = Planner.objects.get(id=pk_input)
            plan_output.delNode(target_id)
            target.contents = plan_output.getString()
            target.save()

            pk_output = callPlan(pk_input)
            plan_output = toPlan(pk_output.contents)
            plan_output.userId = pk_output.user

            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

        if 'search-key' in request.POST and request.POST['search-key']:
            siteKey = request.POST['search-key']
            print(siteKey)
            api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

            results_tmp = searchByKeyword(siteKey, api_tmp)
            print(results_tmp)
            results_list = []
            for elm in results_tmp:
                elm_tmp = getInfos(elm)
                dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid')}
                results_list.append(dic_tmp)
            # output_list = checkInfos(result_list, 'title')
            
            print(results_list)
            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'site_searched':results_list, 'pk_userplan':pk_input,})
        
        return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

    else:
        return render(request, 'planner/reviseplan.html')


# 문자열 전처리용 함수, rating용(value가 integer)
def toDict(string):
    dic = {}
    str_tmp = string[1:len(string)-1].replace('"','')
    str_list = str_tmp.split(",")
    for elm in str_list:
        elm_tmp = elm.split(":")
        dic[elm_tmp[0]] = int(elm_tmp[1])
    return dic



def rankplan(request):
    if 'pk_rating' in request.POST and request.POST['pk_rating']:
        pk_input = request.POST.get('pk_rating')
        pk_output = callPlan(pk_input)

        if pk_output.rating == True:
            return redirect('createplan')
        
        else:
            # 객체 생성
            plan_output = toPlan(pk_output.contents)
            plan_output.userId = pk_output.user

            return render(request, 'planner/rankplan.html', {'plan_to_rank':plan_output, 'pk_rating':pk_input,})
    
    
    if 'ratings' in request.POST and (request.POST['ratings'] != '{}'):
            datas = toDict(request.POST.get('ratings'))
            dis_user = Profile.objects.get(user=request.user)


            dis_type = dis_user.disability 
            pre_type = dis_user.preference
            user_name = request.user

            api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

            preference_types = (
                ('A0101', '자연관광지'),
                ('A0102', '관광자원'),
                ('A0201', '역사관광지'),
                ('A0202', '휴양관광지'),
                ('A0203', '체험관광지'),
                ('A0204', '산업관광지'),
                ('A0205', '건축/조형물'),
                ('A0206', '문화시설'),
                ('A0207', '축제'),
                ('A0208', '공연/행사'),
            )
            
            for key, value in datas.items():
                
                tour_tmp = tourReq('ETC', 'AppTest', api_tmp.mykey)
                tour_tmp.addPara('contentId', key)
                tour_tmp.addPara('catcodeYN', 'Y')
                tour_tmp.addPara('defaultYN', 'Y')
                req_tmp = tour_tmp.makeReq(api_tmp.url, 'detailCommon')

                tmp = requests.get(req_tmp)
                soup = BeautifulSoup(tmp.content, 'html.parser')

                title_tmp = str(soup.find_all('title'))
                cat_tmp = str(soup.find_all('cat2'))


                site_id = key
                site_grade = int(value)
                site_name = getInfos(title_tmp).get('title')
                cat_value = getInfos(cat_tmp).get('cat2')
                cat_value_list = cat_value.split(', ')

                for i in range(len(cat_value_list)):
                    for j in preference_types:
                        if j[0] == cat_value_list[i]:
                            cat_value_list[i] = j[1]
                cat_value = ', '.join(cat_value_list)

                # db 저장부
                Rating(contentId=site_id, contentName=site_name, contentType=cat_value, userRated=user_name, userDType=dis_type, userPType=pre_type, grade=site_grade).save()
            pk_rating = request.POST.get('pk_rating')
            rated_plan = Planner.objects.get(id=pk_rating)
            print(rated_plan)
            rated_plan.rating = True
            rated_plan.save()

            return redirect('createplan')
        

    else:
        return render(request, 'planner/rankplan.html')
    

def viewmap(request):
    if 'pk_userplan' in request.POST and request.POST['pk_userplan']:
        pk_input = request.POST.get('pk_userplan')
        pk_output_ = callPlan(pk_input) #일정 객체 불러옴
        pk_output = toPlan(pk_output_.contents)

        #시작점, 끝점 표시
        pk_output.plan[0].item['siteType'] = int(0)
        pk_output.plan[-1].item['siteType'] = int(2)

        #변수반환: 리스트(장소단위, 장소마다 x,y,장소속성 키 가짐)
        sites_list = []

        #노드별 x, y좌표 취합
        for nodes in pk_output.plan:
            tmp_id = nodes.item.get('siteId')
            node_dict = getGeoInfos(tmp_id)
            
            #장소 속성 명시
            if nodes.item.get('siteType') == 0:
                node_dict['type'] = 0
                start_point = node_dict
            elif nodes.item.get('siteType') == 2:
                node_dict['type'] = 2
                end_point = node_dict
            else:
                node_dict['type'] = 1
                sites_list.append(node_dict)
            
        print(sites_list, start_point, end_point)
        centerx = (start_point.get('mapx') + end_point.get('mapx'))/2 
        centery = (start_point.get('mapy') + end_point.get('mapy'))/2
        center_point = {'mapx':centerx, 'mapy':centery}
        # 장소정보 취합 완료

        return render(request, 'planner/makemap.html', {'sites_list': sites_list, 'start_point':start_point, 'end_point':end_point, 'center_point':center_point,})

    else:
        return render(request, 'planner/makemap.html')

