from django.urls import path

from . import views

list_parties_urlpatterns = [
    path("", views.PartyListPage.as_view(), name="page_party_list")
]

new_party_urlpatterns = [
    path("party/new/", views.page_new_party, name="page_new_party"),
    path(
        "party/new/check-date/",
        views.partial_check_party_date,
        name="partial_check_party_date",
    ),
    path(
        "party/new/check-invitation/",
        views.partial_check_invitation,
        name="partial_check_invitation",
    ),
]

party_detail_urlpatterns = [
    path(
        "party/<uuid:party_uuid>/",
        views.PartyDetailPage.as_view(),
        name="page_single_party",
    ),
    path(
        "party/<uuid:party_uuid>/details/",
        views.PartyDetailPartial.as_view(),
        name="partial_party_detail",
    ),
]


urlpatterns = (
    list_parties_urlpatterns + new_party_urlpatterns + party_detail_urlpatterns
)
