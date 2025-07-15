from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from chamas.models import ChamaMembership
from finance.models import Contribution, Loan

# landing page
class LandingPageView(TemplateView):

    template_name = 'landing.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        membership = ChamaMembership.objects.select_related('chama').filter(user=user).first()
        context['in_chama'] = bool(membership)

        if membership:
            chama = membership.chama
            now = timezone.now()
            total_savings = Contribution.objects.filter(chama=chama).aggregate(total=Sum('amount'))['total'] or 0
            user_contributions = Contribution.objects.filter(
                member=user, chama=chama,
                date__year=now.year, date__month=now.month
            ).aggregate(total=Sum('amount'))['total'] or 0

            user_loans = Loan.objects.filter(
    borrower=user,
    chama=chama,
).exclude(status='repaid').aggregate(
    total=Sum('amount')
)['total'] or 0

            goal = chama.goal_amount or 1
            progress = round((total_savings / goal) * 100, 1)

            members = ChamaMembership.objects.select_related('user').filter(chama=chama)

            recent_contributions = Contribution.objects.filter(chama=chama).order_by('-date')[:5]
            recent_loans = Loan.objects.filter(chama=chama).order_by('-requested_at')[:5]

            context.update({
    'chama': chama,
    'user_role': membership.get_role_display(),
    'total_savings': total_savings,
    'user_contributions': user_contributions,
    'user_loans': user_loans,
    'goal_progress': progress,
    'members': members,
    'recent_contributions': recent_contributions,
    'recent_loans': recent_loans,
    'invite_code': chama.invite_code,
})

        return context
    
