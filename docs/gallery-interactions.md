# Gallery Interactions Feature

## Overview
Like and comment functionality for gallery items. **Likes and comments are visible to all users** (both logged-in and non-logged-in), but **only authenticated users can interact** (like/unlike items and post comments). Non-authenticated users who try to interact will be redirected to the login page.

## Implementation Details

### Models

#### GalleryLike
- **Purpose**: Tracks which users have liked which gallery items
- **Fields**:
  - `gallery_item`: ForeignKey to GalleryImage
  - `user`: ForeignKey to User
  - `created_at`: DateTimeField (auto-generated)
- **Constraints**: Unique together on `gallery_item` and `user` (prevents duplicate likes)
- **Related Name**: `likes` on GalleryImage

#### GalleryComment
- **Purpose**: Stores user comments on gallery items
- **Fields**:
  - `gallery_item`: ForeignKey to GalleryImage
  - `user`: ForeignKey to User
  - `text`: TextField (comment content)
  - `created_at`: DateTimeField (auto-generated)
- **Related Name**: `comments` on GalleryImage

### Views

#### `toggle_like(request, item_id)`
- **Method**: POST only
- **Authentication**: Required (login_required)
- **Purpose**: Toggle like status for a gallery item
- **Returns**: JSON response with `success`, `is_liked`, and `like_count`
- **Behavior**: Creates like if doesn't exist, deletes if exists

#### `add_comment(request, item_id)`
- **Method**: POST only
- **Authentication**: Required (login_required)
- **Purpose**: Add a new comment to a gallery item
- **Parameters**: `text` (required)
- **Returns**: JSON response with `success`, `comment` object, and `comment_count`
- **Validation**: Returns 400 if text is empty

#### `get_comments(request, item_id)`
- **Method**: GET
- **Authentication**: Not required (public)
- **Purpose**: Retrieve comments for a gallery item
- **Returns**: JSON response with `success`, `comments` array, and `comment_count`
- **Limit**: Returns latest 10 comments

#### Updated `gallery(request)`
- **Enhancement**: Now includes like/comment counts and user like status
- **Context**: Each gallery item has:
  - `like_count`: Number of likes
  - `comment_count`: Number of comments
  - `is_liked`: Boolean indicating if current user has liked the item

### URLs

- `/gallery/<item_id>/like/` - Toggle like (POST, login required)
- `/gallery/<item_id>/comment/` - Add comment (POST, login required)
- `/gallery/<item_id>/comments/` - Get comments (GET, public)

### Frontend Implementation

#### UI Components
- **Like Button**: Appears on gallery items (bottom-left) for **all users**
  - Shows heart icon and like count (visible to everyone)
  - Changes color when liked (for authenticated users)
  - Has hover animation
  - Disabled state for non-authenticated users (redirects to login on click)
- **Comment Button**: Appears next to like button for **all users**
  - Shows comment icon and comment count (visible to everyone)
  - Opens comment modal on click (for authenticated users)
  - Disabled state for non-authenticated users (redirects to login on click)
- **Comment Modal**: Full-screen modal dialog
  - Shows list of comments (visible to everyone)
  - Has comment form at bottom (only for authenticated users)
  - Shows login prompt for non-authenticated users
  - Closable via X button or clicking outside
- **Emoji Picker**: Instagram-style emoji selector
  - Accessible via emoji button (😊) next to comment textarea
  - Contains 70+ popular Instagram-style emojis
  - Grid layout with categories (hearts, faces, food, travel, etc.)
  - Click to insert emoji at cursor position
  - Closes when clicking outside or on close button
  - Smooth slide-up animation

#### JavaScript Features
- **AJAX Requests**: All interactions use fetch API
- **CSRF Token**: Retrieved from cookies
- **Real-time Updates**: Like/comment counts update without page refresh
- **Event Handling**: Prevents lightbox from opening when clicking interaction buttons
- **Emoji Picker**: Custom emoji selector with 70+ popular emojis
  - Toggle button to show/hide picker
  - Click emoji to insert at cursor position
  - Closes on outside click or close button
  - Smooth animations

### CSS Styling

- **Interaction Buttons**: Styled with white background, rounded corners, shadow
- **Liked State**: Red background with white text
- **Comment Modal**: Centered, responsive, with scrollable comment list
- **Animations**: Heart beat animation on like, smooth transitions

## Files Involved

### Backend
- `website/models.py` - GalleryLike and GalleryComment models
- `website/views.py` - View functions for interactions
- `website/urls.py` - URL routing
- `website/admin.py` - Admin registration for new models

### Frontend
- `website/templates/website/gallery.html` - Template with UI and JavaScript
- `static/css/style.css` - Styling for interactions and modal

### Database
- Migration: `website/migrations/0003_gallerycomment_gallerylike.py`

## Usage

### For Users
1. **Liking**: Click the heart button on any gallery item
2. **Commenting**: Click the comment button, type your comment, and submit
3. **Viewing Comments**: Click comment button to see all comments

### For Developers
- All interactions require authentication
- Like/unlike is a toggle operation
- Comments are displayed in reverse chronological order (newest first)
- Comment form validates for empty text

## Important Notes

- **Visibility**: Likes and comments are **visible to everyone** (logged-in and non-logged-in users)
- **Interaction**: Only **authenticated users** can like/unlike items and post comments
- **Non-authenticated Users**: Clicking like/comment buttons redirects to login page with return URL
- **CSRF Protection**: All POST requests include CSRF token
- **Unique Likes**: Users can only like an item once (toggle behavior)
- **No Comment Limits**: Users can post multiple comments on the same item
- **Comment Display**: Shows latest 10 comments in modal (visible to everyone)
- **Real-time Updates**: Counts update immediately after actions
- **UI Feedback**: Disabled buttons have reduced opacity and show tooltip on hover

## Future Enhancements

- Comment pagination for items with many comments
- Comment editing/deletion
- Like notifications
- Comment replies/threading
- Comment moderation

