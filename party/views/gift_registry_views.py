from django.http import QueryDict
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView

from party.forms import GiftForm
from party.models import Gift, Party


class GiftRegistryPage(ListView):
    model = Gift
    template_name = "party/gift_registry/page_gift_registry.html"
    context_object_name = "gifts"

    def get_queryset(self):
        return Gift.objects.filter(party_id=self.kwargs["party_uuid"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party"] = Party.objects.get(uuid=self.kwargs["party_uuid"])
        return context


class GiftDetailPartial(DetailView):
    model = Gift
    template_name = "party/gift_registry/partial_gift_detail.html"
    context_object_name = "gift"
    pk_url_kwarg = "gift_uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party"] = self.object.party
        return context


class GiftUpdateFormPartial(View):
    def get(self, request, gift_uuid, *args, **kwargs):
        gift = get_object_or_404(Gift, uuid=gift_uuid)
        form = GiftForm(instance=gift)

        return render(
            request,
            "party/gift_registry/partial_gift_update.html",
            {"form": form, "gift": gift},
        )

    def put(self, request, gift_uuid, *args, **kwargs):
        data = QueryDict(request.body).dict()
        gift = Gift.objects.get(uuid=gift_uuid)
        form = GiftForm(data, instance=gift)

        if form.is_valid():
            form.save()

            return render(
                request,
                "party/gift_registry/partial_gift_detail.html",
                {"gift": gift, "party": gift.party},
            )

        return render(
            request,
            "party/gift_registry/partial_gift_update.html",
            {"form": form, "gift": gift},
        )
