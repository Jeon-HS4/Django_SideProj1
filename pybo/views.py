from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone

from pybo.forms import QuestionForm
from .models import Question
from datetime import date,timedelta,datetime
from calendar import monthrange



def main(request):
    current_datetime = timezone.now()
    default_year = current_datetime.year
    default_month = current_datetime.month
    
    year = int(request.GET.get('years',default_year)) # 해당 년 정보
    month = int(request.GET.get('month',default_month)) # 해당 월 정보  
    
    start_date = date(year, month, 1)  # 2023년 6월 1일
    if(month != 12):
        end_date = date(year, month+1, 1) - timedelta(days=1)
    else:
        end_date = date(year+1, 1, 1)
        
    diary_list = Question.objects.filter(write_date__range=(start_date, end_date)).values()

    calendar_weeks = get_calendar_data(year, month)

    addcontext = {}
    if diary_list:
        for diary in diary_list:
            cnt = 1
            day = str((diary['write_date'] + timedelta(hours=9)).day) + " " +str(cnt)
            if(day in addcontext):
                cnt += 1
                day = str(diary['write_date'].day) + " " +str(cnt)
            addcontext[day] = diary
            addcontext[day]['write_date'] = addcontext[day]['write_date'].isoformat()

    context = {'diary_list': diary_list, 'daily_write': addcontext, 'calendar_weeks': calendar_weeks}
    
    return render(request, 'pybo/diary_main.html', context)



def get_calendar_data(year, month):
    calendar_weeks = []

    # 해당 월의 일수 및 시작일
    num_days = monthrange(year, month)[1]
    start_date = date(year, month, 1)

    # 앞 뒤로 추가적으로 표시할 일 수
    prev_month_end_day = start_date - timedelta(days=1)
    next_month_start_day = start_date + timedelta(days=num_days)
    num_days_prev_month = prev_month_end_day.weekday()+1 if prev_month_end_day.weekday() != 6 else 0
    num_days_next_month = 7 - next_month_start_day.weekday() if next_month_start_day.weekday() != 6 else 0

    # 총 표시해야 할 일/주 수
    total_days =  num_days_prev_month + num_days + num_days_next_month
    num_weeks = total_days // 7 + (1 if total_days % 7 != 0 else 0)

    for week in range(num_weeks):
        week_days = []
        for day in range(7):
            # 현재 일자
            current_date = start_date + timedelta(days=(day - start_date.weekday()-1) + (week * 7))

            is_current_month = current_date.month == month
            
            dayOfWeek = day

            day_data = {
                'date': current_date,
                'is_current_month': is_current_month,
                'dayOfWeek': dayOfWeek
            }
            week_days.append(day_data)
        calendar_weeks.append(week_days)

    return calendar_weeks

def diary_detail(request, dates, key):
    
    dates = datetime.strptime(dates, '%Y-%m-%d').date()

    context_list = Question.objects.filter(write_date__date=dates).order_by('write_date')
    detail_context = context_list[int(key)-1]
    
    context = {'detail_context': detail_context, 'data_key':key}

    return render(request,'pybo/diary_detail.html', context)


def diary_modify_form(request, dates, key):
    
    dates = datetime.strptime(dates, '%Y-%m-%d').date()

    context_list = Question.objects.filter(write_date__date=dates).order_by('write_date')
    detail_context = context_list[int(key)-1]
    
    context = {'detail_context': detail_context, 'data_key':key}
    
    return render(request, 'pybo/diary_modify.html', context)


def diary_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,"수정 권한이 없습니다")
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)



def diary_delete(request, dates, key):
    dates = datetime.strptime(dates, '%Y-%m-%d').date()
    date_list = dates.split('-')
    delete_object = Question.objects.filter(write_date__date=dates).order_by('write_date')
    delete_object = delete_object[int(key)-1]
    delete_object.delete()
    
    #return redirect('pybo:main')
    return redirect(f'/pybo/?years={date_list[0]}&month={date_list[1]}')


def diary_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.author = 'User'
            years = diary.write_date.year
            month = diary.write_date.month
            diary.save()
            return redirect(f'/pybo/?years={years}&month={month}')
    else:
        form = QuestionForm()
    
    context = {'form': form}
    
    return render(request, 'pybo/diary_create.html', context)