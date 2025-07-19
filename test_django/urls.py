from django.urls import path
from test_django.views.api_views import *
from test_django.views.auth_views import *
from test_django.views.views import *
from test_django.yasg import urlpatterns as api_doc_urls
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from test_django.postvote_views import *
from test_django.views.commentvote_views import *
from test_django.views.chat_views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),

    path("category/<int:pk>/", CategoryPost.as_view(), name="category_post"),
    path("post/<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("add_article/", AddPost.as_view(), name="add"),
    path("post/<int:pk>/update/", PostUpdate.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDelete.as_view(), name="post_delete"),
    path("search/",SearchResults.as_view() , name="search"),
    path("changepass", UserChangePass.as_view(), name="changepass"),
    path("add_category", AddCategory.as_view(), name="add_category"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('login_user')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("comment/<int:pk>/delete/", CommentDelete.as_view(), name="comment_delete"),
    path("comment/<int:pk>/update/", CommentUpdate.as_view(), name="comment_update"),


    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/dislike/', dislike_post, name='dislike_post'),
    path('post/<int:pk>/vote/<str:value>/', vote_post, name='vote_post'),
    path("comment/<int:pk>/like/", like_comment, name="like_comment"),
    path("comment/<int:pk>/dislike/", dislike_post, name="dislike_comment"),
    path("comment/<int:pk>/vote/<str:value>/", vote_comment, name="vote_comment"),
    path("author/<int:user_id>/", AuthorPostsView.as_view(), name="author_posts"),
    path("author/<int:user_id>/category/<int:category_id>/", AuthorCategoryPostsView.as_view(),name="category_post_author"),
    path("login_user/", user_login, name="login_user"),
    path("logout_user/", user_logout, name="logout_user"),
    path("register_user/", register_user, name="register_user"),
    path("add_comment<int:post_id>/", add_comment, name="add_comment"),
    path("profile<int:user_id>/", profile, name="profile"),
    path("subs<int:user_id>/", follow_user, name="follow_user"),
    path("unsub<int:user_id>/", unfollow_user, name="unfollow_user"),
    # path("following_user/<int:pk>/", subscriptions_list, name="subs_list"),
    # path("follow_user/<int:pk>/", subscribers_list, name="sub_list"),
    path("user/<int:pk>/<str:view_type>/", user_detail_list, name="user_detail_list"),
    path("profileform_test", changeprofile, name="profileform_test"),
    path("chat/", chats_view, name="chats_view"),
    path("chat/<username>", get_or_create_chat , name="start_chat"),
    path("chat/room/<chatroom_name>", chats_view, name="chat_rooms"),
    path("my-chats/", my_chats_view, name="your_chats"),
    path("chat/fileupload/<chatroom_name>", chat_file_upload, name="chat_file_upload"),
    path("save-avatar/<int:user_id>/", save_avatar, name="save_avatar"),
    path("post/<int:post_id>/reply/", reply_to_comment, name="reply_to_comment"),
    path('notificated/', notificated_view, name='notificated'),
    path('notificated/mark-read/', mark_notificated_as_read, name='mark_notificated_as_read'),

    #API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path("post/api/", MarketApi.as_view(), name="marketapi"),
    path("post/api/<int:pk>/", MarketDetailApi.as_view(), name="marketdetailapi"),
    path("category/api/", MarketApiCategory.as_view(), name="categoryapi"),
    path("category/api/<int:pk>/", MarketDetailApiCategory.as_view(), name="categorydetailapi"),
    path("catpost/api/<int:pk>/", MarketCategorypost.as_view(), name="catpost"),
]

urlpatterns += api_doc_urls


