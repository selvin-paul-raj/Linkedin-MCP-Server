# src/linkedin_mcp_server/tools/post.py
"""
LinkedIn API tools for posts, media, documents, reactions, and more.

Comprehensive LinkedIn REST API integration supporting:
- Post creation, updates, and deletion
- Image/video/document uploads
- Reactions management
- Complete w_member_social permission coverage
"""

import logging
import os
from enum import Enum
from typing import Any, Dict, List, Optional

import requests
from fastmcp import FastMCP

logger = logging.getLogger(__name__)


class PostVisibility(str, Enum):
    """LinkedIn post visibility options."""

    PUBLIC = "PUBLIC"
    CONNECTIONS = "CONNECTIONS"


class ReactionType(str, Enum):
    """LinkedIn reaction types."""

    LIKE = "LIKE"
    PRAISE = "PRAISE"
    APPRECIATION = "APPRECIATION"
    EMPATHY = "EMPATHY"
    INTEREST = "INTEREST"
    ENTERTAINMENT = "ENTERTAINMENT"


class LinkedInAPIClient:
    """Comprehensive LinkedIn REST API client."""

    def __init__(self, access_token: str, base_url: Optional[str] = None):
        """
        Initialize LinkedIn API client.

        Args:
            access_token (str): LinkedIn API access token
            base_url (str, optional): Base URL for REST API
        """
        self.access_token = access_token
        self.base_url = base_url or os.getenv(
            "LINKEDIN_API_BASE_URL", "https://api.linkedin.com/rest"
        )
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": os.getenv("LINKEDIN_API_VERSION", "202405"),
            "X-Restli-Protocol-Version": "2.0.0",
        }
        self._person_urn = None

    def _get_person_urn(self) -> str:
        """Get cached person URN or fetch it."""
        if self._person_urn:
            return self._person_urn

        try:
            # Use /v2/userinfo endpoint (works with w_member_social)
            response = requests.get(
                "https://api.linkedin.com/v2/userinfo",
                headers=self.headers,
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                person_id = data.get("sub")
                if person_id:
                    self._person_urn = f"urn:li:person:{person_id}"
                    logger.info(f"Got person URN: {self._person_urn}")
                    return self._person_urn
        except Exception as e:
            logger.warning(f"Failed to get person URN from userinfo: {e}")

        try:
            # Fallback: Try /rest/me endpoint
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers,
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                person_id = data.get("id") or data.get("sub")
                if person_id:
                    self._person_urn = f"urn:li:person:{person_id}"
                    logger.info(f"Got person URN from /rest/me: {self._person_urn}")
                    return self._person_urn
        except Exception as e:
            logger.warning(f"Failed to get person URN from /rest/me: {e}")

        raise Exception(
            "Cannot determine user ID. Ensure you have w_member_social permission."
        )

    # ==================== POST MANAGEMENT ====================

    def create_post(
        self,
        text: str,
        visibility: PostVisibility = PostVisibility.PUBLIC,
        media_urns: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a LinkedIn post (text, image, video, or document).

        Args:
            text: Post content
            visibility: PUBLIC or CONNECTIONS
            media_urns: Optional list of media URNs (images/videos/documents)

        Returns:
            Dict with post URN and status
        """
        author_urn = self._get_person_urn()

        post_data = {
            "author": author_urn,
            "commentary": text,
            "visibility": visibility.value,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        # Add media if provided
        if media_urns:
            post_data["content"] = {"media": {"id": media_urns[0]}}

        try:
            logger.info("Creating LinkedIn post")
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=post_data,
                timeout=15,
            )
            response.raise_for_status()

            result = response.json()
            post_urn = result.get("id", result.get("urn", "unknown"))

            logger.info(f"Post created: {post_urn}")
            return {"post_urn": post_urn, "status": "success", "data": result}
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to create post: {str(e)}"
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data}"
                except Exception:
                    error_msg += f" - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def update_post(self, post_urn: str, text: str) -> Dict[str, Any]:
        """
        Update an existing LinkedIn post.

        Args:
            post_urn: URN of the post to update
            text: New post content

        Returns:
            Dict with status
        """
        try:
            patch_data = {"commentary": text}

            response = requests.patch(
                f"{self.base_url}/posts/{post_urn}",
                headers=self.headers,
                json={"patch": {"$set": patch_data}},
                timeout=15,
            )
            response.raise_for_status()

            logger.info(f"Post updated: {post_urn}")
            return {"status": "success", "message": "Post updated successfully"}
        except Exception as e:
            logger.error(f"Failed to update post: {e}")
            raise Exception(f"Failed to update post: {str(e)}")

    def delete_post(self, post_urn: str) -> Dict[str, Any]:
        """
        Delete a LinkedIn post.

        Args:
            post_urn: URN of the post to delete

        Returns:
            Dict with status
        """
        try:
            response = requests.delete(
                f"{self.base_url}/posts/{post_urn}",
                headers=self.headers,
                timeout=15,
            )
            response.raise_for_status()

            logger.info(f"Post deleted: {post_urn}")
            return {"status": "success", "message": "Post deleted successfully"}
        except Exception as e:
            logger.error(f"Failed to delete post: {e}")
            raise Exception(f"Failed to delete post: {str(e)}")

    # ==================== IMAGE MANAGEMENT ====================

    def initialize_image_upload(self) -> Dict[str, Any]:
        """
        Initialize image upload to LinkedIn.

        Returns:
            Dict with upload URL and image URN
        """
        author_urn = self._get_person_urn()

        try:
            response = requests.post(
                f"{self.base_url}/images?action=initializeUpload",
                headers=self.headers,
                json={"initializeUploadRequest": {"owner": author_urn}},
                timeout=15,
            )
            response.raise_for_status()

            result = response.json()
            return {
                "upload_url": result.get("value", {}).get("uploadUrl"),
                "image_urn": result.get("value", {}).get("image"),
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Failed to initialize image upload: {e}")
            raise Exception(f"Failed to initialize image upload: {str(e)}")

    def upload_image(self, image_url: str) -> Dict[str, Any]:
        """
        Complete image upload workflow.

        Args:
            image_url: URL of the image to upload

        Returns:
            Dict with image URN
        """
        # Initialize upload
        init_result = self.initialize_image_upload()
        upload_url = init_result["upload_url"]
        image_urn = init_result["image_urn"]

        try:
            # Download image
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            # Upload to LinkedIn
            upload_response = requests.put(
                upload_url, data=img_response.content, timeout=30
            )
            upload_response.raise_for_status()

            logger.info(f"Image uploaded: {image_urn}")
            return {"image_urn": image_urn, "status": "success"}
        except Exception as e:
            logger.error(f"Failed to upload image: {e}")
            raise Exception(f"Failed to upload image: {str(e)}")

    def get_image(self, image_id: str) -> Dict[str, Any]:
        """Get image details."""
        try:
            response = requests.get(
                f"{self.base_url}/images/{image_id}", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            raise Exception(f"Failed to get image: {str(e)}")

    # ==================== VIDEO MANAGEMENT ====================

    def initialize_video_upload(self, file_size: int) -> Dict[str, Any]:
        """
        Initialize video upload.

        Args:
            file_size: Size of video file in bytes

        Returns:
            Dict with upload instructions and video URN
        """
        author_urn = self._get_person_urn()

        try:
            response = requests.post(
                f"{self.base_url}/videos?action=initializeUpload",
                headers=self.headers,
                json={
                    "initializeUploadRequest": {
                        "owner": author_urn,
                        "fileSizeBytes": file_size,
                        "uploadCaptions": False,
                        "uploadThumbnail": False,
                    }
                },
                timeout=15,
            )
            response.raise_for_status()

            result = response.json()
            return {
                "upload_instructions": result.get("value", {}).get(
                    "uploadInstructions"
                ),
                "video_urn": result.get("value", {}).get("video"),
                "status": "success",
            }
        except Exception as e:
            raise Exception(f"Failed to initialize video upload: {str(e)}")

    def finalize_video_upload(
        self, video_urn: str, upload_token: str, etags: List[str]
    ) -> Dict[str, Any]:
        """
        Finalize video upload after chunks are uploaded.

        Args:
            video_urn: Video URN from initialization
            upload_token: Upload token from initialization
            etags: List of ETags from chunk uploads

        Returns:
            Dict with status
        """
        try:
            response = requests.post(
                f"{self.base_url}/videos?action=finalizeUpload",
                headers=self.headers,
                json={
                    "finalizeUploadRequest": {
                        "video": video_urn,
                        "uploadToken": upload_token,
                        "uploadedPartIds": etags,
                    }
                },
                timeout=15,
            )
            response.raise_for_status()

            return {"status": "success", "message": "Video upload finalized"}
        except Exception as e:
            raise Exception(f"Failed to finalize video upload: {str(e)}")

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video details."""
        try:
            response = requests.get(
                f"{self.base_url}/videos/{video_id}", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            raise Exception(f"Failed to get video: {str(e)}")

    # ==================== DOCUMENT MANAGEMENT ====================

    def initialize_document_upload(self) -> Dict[str, Any]:
        """Initialize document upload."""
        author_urn = self._get_person_urn()

        try:
            response = requests.post(
                f"{self.base_url}/documents?action=initializeUpload",
                headers=self.headers,
                json={"initializeUploadRequest": {"owner": author_urn}},
                timeout=15,
            )
            response.raise_for_status()

            result = response.json()
            return {
                "upload_url": result.get("value", {}).get("uploadUrl"),
                "document_urn": result.get("value", {}).get("document"),
                "status": "success",
            }
        except Exception as e:
            raise Exception(f"Failed to initialize document upload: {str(e)}")

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document details."""
        try:
            response = requests.get(
                f"{self.base_url}/documents/{document_id}",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            raise Exception(f"Failed to get document: {str(e)}")

    # ==================== REACTIONS ====================

    def add_reaction(self, entity_urn: str, reaction_type: ReactionType) -> Dict[str, Any]:
        """
        Add a reaction to a post or comment.

        Args:
            entity_urn: URN of the entity to react to
            reaction_type: Type of reaction (LIKE, PRAISE, etc.)

        Returns:
            Dict with status
        """
        author_urn = self._get_person_urn()

        try:
            response = requests.post(
                f"{self.base_url}/reactions",
                headers=self.headers,
                json={
                    "actor": author_urn,
                    "object": entity_urn,
                    "reactionType": reaction_type.value,
                },
                timeout=15,
            )
            response.raise_for_status()

            return {"status": "success", "message": f"Reaction {reaction_type.value} added"}
        except Exception as e:
            raise Exception(f"Failed to add reaction: {str(e)}")

    def remove_reaction(self, reaction_id: str) -> Dict[str, Any]:
        """Remove a reaction."""
        try:
            response = requests.delete(
                f"{self.base_url}/reactions/{reaction_id}",
                headers=self.headers,
                timeout=15,
            )
            response.raise_for_status()

            return {"status": "success", "message": "Reaction removed"}
        except Exception as e:
            raise Exception(f"Failed to remove reaction: {str(e)}")

    def get_reactions(self, entity_urn: str) -> Dict[str, Any]:
        """Get reactions for an entity."""
        try:
            response = requests.get(
                f"{self.base_url}/reactions",
                headers=self.headers,
                params={"q": "entity", "entity": entity_urn},
                timeout=10,
            )
            response.raise_for_status()

            return {"status": "success", "data": response.json()}
        except Exception as e:
            raise Exception(f"Failed to get reactions: {str(e)}")

    # ==================== PROFILE & VALIDATION ====================

    def get_profile(self) -> Dict[str, Any]:
        """Get authenticated user's profile (requires r_liteprofile permission)."""
        try:
            # Try /rest/me endpoint
            response = requests.get(f"{self.base_url}/me", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {"status": "success", "profile": data}
            elif response.status_code == 403:
                # Token doesn't have profile read permission
                return {
                    "status": "limited",
                    "message": "Profile access requires r_liteprofile permission. Your token has w_member_social (post creation) only.",
                    "person_urn": self._person_urn or "Call validate_credentials first",
                }
            else:
                response.raise_for_status()
        except Exception as e:
            logger.warning(f"Failed to get profile: {e}")
            return {
                "status": "limited",
                "message": f"Profile access limited: {str(e)}",
                "person_urn": self._person_urn or "Unknown",
            }

    def validate_credentials(self) -> bool:
        """Validate API credentials by testing access."""
        try:
            # Try to get person URN - this works with w_member_social
            self._get_person_urn()
            return True
        except Exception as e:
            logger.error(f"Credential validation failed: {e}")
            return False


def register_post_tools(mcp: FastMCP) -> None:
    """Register all LinkedIn API tools with the MCP server."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

    if not access_token:
        logger.warning(
            "LINKEDIN_ACCESS_TOKEN not found. API tools disabled. "
            "Set LINKEDIN_ACCESS_TOKEN environment variable to enable."
        )
        return

    client = LinkedInAPIClient(access_token)
    logger.info("✓ LinkedIn API tools enabled")

    # ==================== POST TOOLS ====================

    @mcp.tool()
    async def create_linkedin_post(
        text: str, visibility: str = "PUBLIC", image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a LinkedIn post (text or with image).

        Args:
            text: Post content text
            visibility: 'PUBLIC' or 'CONNECTIONS' (default: PUBLIC)
            image_url: Optional image URL to include

        Returns:
            Dict with post URN and status
        """
        try:
            vis = PostVisibility.PUBLIC if visibility.upper() != "CONNECTIONS" else PostVisibility.CONNECTIONS

            media_urns = None
            if image_url:
                upload_result = client.upload_image(image_url)
                media_urns = [upload_result["image_urn"]]

            result = client.create_post(text, vis, media_urns)
            return {"status": "success", "post_urn": result["post_urn"], "message": "Post created successfully"}
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def update_linkedin_post(post_urn: str, text: str) -> Dict[str, Any]:
        """
        Update an existing LinkedIn post.

        Args:
            post_urn: URN of the post to update (e.g., 'urn:li:share:123456')
            text: New post content

        Returns:
            Dict with status
        """
        try:
            result = client.update_post(post_urn, text)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def delete_linkedin_post(post_urn: str) -> Dict[str, Any]:
        """
        Delete a LinkedIn post.

        Args:
            post_urn: URN of the post to delete

        Returns:
            Dict with status
        """
        try:
            result = client.delete_post(post_urn)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ==================== IMAGE TOOLS ====================

    @mcp.tool()
    async def upload_linkedin_image(image_url: str) -> Dict[str, Any]:
        """
        Upload an image to LinkedIn.

        Args:
            image_url: URL of the image to upload

        Returns:
            Dict with image URN for use in posts
        """
        try:
            result = client.upload_image(image_url)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_linkedin_image(image_id: str) -> Dict[str, Any]:
        """
        Get LinkedIn image details.

        Args:
            image_id: Image ID or URN

        Returns:
            Dict with image data
        """
        try:
            result = client.get_image(image_id)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ==================== REACTION TOOLS ====================

    @mcp.tool()
    async def add_linkedin_reaction(
        entity_urn: str, reaction_type: str = "LIKE"
    ) -> Dict[str, Any]:
        """
        Add a reaction to a LinkedIn post.

        Args:
            entity_urn: URN of the post/comment to react to
            reaction_type: LIKE, PRAISE, APPRECIATION, EMPATHY, INTEREST, or ENTERTAINMENT

        Returns:
            Dict with status
        """
        try:
            reaction = ReactionType[reaction_type.upper()]
            result = client.add_reaction(entity_urn, reaction)
            return result
        except KeyError:
            return {
                "status": "error",
                "message": f"Invalid reaction type. Use: {', '.join([r.name for r in ReactionType])}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def remove_linkedin_reaction(reaction_id: str) -> Dict[str, Any]:
        """
        Remove a reaction from LinkedIn.

        Args:
            reaction_id: ID of the reaction to remove

        Returns:
            Dict with status
        """
        try:
            result = client.remove_reaction(reaction_id)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_linkedin_reactions(entity_urn: str) -> Dict[str, Any]:
        """
        Get reactions for a LinkedIn entity.

        Args:
            entity_urn: URN of the post/comment

        Returns:
            Dict with reactions data
        """
        try:
            result = client.get_reactions(entity_urn)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ==================== PROFILE TOOLS ====================

    @mcp.tool()
    async def get_linkedin_profile() -> Dict[str, Any]:
        """
        Get your authenticated LinkedIn profile.

        Returns:
            Dict with profile data
        """
        try:
            result = client.get_profile()
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def validate_linkedin_credentials() -> Dict[str, Any]:
        """
        Validate LinkedIn API credentials.

        Returns:
            Dict with validation status
        """
        try:
            is_valid = client.validate_credentials()
            if is_valid:
                return {
                    "status": "success",
                    "message": "LinkedIn credentials are valid",
                }
            else:
                return {
                    "status": "error",
                    "message": "LinkedIn credentials validation failed",
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
