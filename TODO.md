# TODO: Fix Social Media API Feed Implementation

## Information Gathered:
- Post model currently uses `user` field instead of `author` field
- FeedAPIView is correctly implemented but uses `user` field
- Test expects `author__in=following_users` pattern
- Accounts URLs already have follow/unfollow routes: `/follow/<int:user_id>/` and `/unfollow/<int:user_id>/`
- Posts URLs already have `/feed/` route

## Plan:
1. **Update Post model**: Change `user` field to `author` field
2. **Update all Post-related code** that references the old `user` field:
   - posts/models.py (Post model)
   - posts/views.py (FeedAPIView and other views)
   - posts/serializers.py (PostSerializer)
   - posts/admin.py (if any references)
3. **Update PostQuerySet references** in views to use `author` field
4. **Run migrations** to apply the field change
5. **Test the implementation** to ensure it works correctly

## Files to Edit:
- social_media_api/posts/models.py
- social_media_api/posts/views.py  
- social_media_api/posts/serializers.py
- social_media_api/posts/admin.py (if needed)

## Follow-up Steps:
- Run Django migrations
- Test the feed endpoint
- Verify follow/unfollow functionality works with new author field
