"""
Test suite for performance optimizations and bug fixes.
Tests critical bug fixes in validators and common validator functionality.
"""

import pytest
from datetime import datetime, timedelta
from stidantic.types import Hashes, StixDomain
from stidantic.sdo import Campaign
from stidantic.validators import validate_hex_field, validate_bin_field
from pydantic import ValidationInfo


class TestCriticalBugFixes:
    """Test critical bugs that were fixed."""
    
    def test_hex_field_validator_fix(self):
        """Test that hex field validator correctly checks field name."""
        # Mock ValidationInfo
        class MockInfo:
            field_name = "test_hex"
        
        # Should NOT raise error when field ends with _hex
        result = validate_hex_field("abcd1234", MockInfo())
        assert result == "abcd1234"
        
        # Should raise error when field does NOT end with _hex
        class MockInfoBad:
            field_name = "test_bad"
        
        with pytest.raises(ValueError, match="property name MUST end with '_hex'"):
            validate_hex_field("abcd1234", MockInfoBad())
    
    def test_bin_field_validator(self):
        """Test that bin field validator correctly checks field name."""
        # Mock ValidationInfo
        class MockInfo:
            field_name = "test_bin"
        
        # Should NOT raise error when field ends with _bin
        result = validate_bin_field("data", MockInfo())
        assert result == "data"
        
        # Should raise error when field does NOT end with _bin
        class MockInfoBad:
            field_name = "test_bad"
        
        with pytest.raises(ValueError, match="property name MUST end with '_bin'"):
            validate_bin_field("data", MockInfoBad())
    
    def test_hashes_validation_fix(self):
        """Test that Hashes validates extra keys correctly."""
        # Valid extra hash with proper key
        valid_hash = Hashes(
            sha256="abc123",
            **{"custom-hash": "value123"}  # Valid: 3-250 chars, matches pattern
        )
        assert valid_hash.sha256 == "abc123"
        
        # Invalid: key too short (less than 3 chars)
        with pytest.raises(ValueError, match="Invalid extra hash key"):
            Hashes(sha256="abc123", **{"ab": "value123"})
        
        # Invalid: key too long (more than 250 chars)
        with pytest.raises(ValueError, match="Invalid extra hash key"):
            Hashes(sha256="abc123", **{"a" * 251: "value123"})


class TestCommonValidators:
    """Test common validator factory functions."""
    
    def test_first_last_seen_validator(self):
        """Test that first/last seen validator works correctly."""
        now = datetime.now()
        past = now - timedelta(days=1)
        future = now + timedelta(days=1)
        
        # Valid: last_seen after first_seen
        valid_campaign = Campaign(
            id="campaign--12345678-1234-1234-1234-123456789012",
            created=now,
            modified=now,
            name="Test Campaign",
            first_seen=past,
            last_seen=now
        )
        assert valid_campaign.first_seen == past
        assert valid_campaign.last_seen == now
        
        # Valid: last_seen equals first_seen
        valid_campaign2 = Campaign(
            id="campaign--12345678-1234-1234-1234-123456789013",
            created=now,
            modified=now,
            name="Test Campaign 2",
            first_seen=now,
            last_seen=now
        )
        assert valid_campaign2.first_seen == now
        assert valid_campaign2.last_seen == now
        
        # Invalid: last_seen before first_seen
        with pytest.raises(ValueError, match="last_seen property MUST be greater than or equal"):
            Campaign(
                id="campaign--12345678-1234-1234-1234-123456789014",
                created=now,
                modified=now,
                name="Invalid Campaign",
                first_seen=future,
                last_seen=past
            )
    
    def test_modified_after_created_validator(self):
        """Test that modified after created validator works correctly."""
        now = datetime.now()
        past = now - timedelta(days=1)
        future = now + timedelta(days=1)
        
        # Valid: modified after created
        valid_campaign = Campaign(
            id="campaign--12345678-1234-1234-1234-123456789015",
            created=past,
            modified=now,
            name="Test Campaign"
        )
        assert valid_campaign.created == past
        assert valid_campaign.modified == now
        
        # Valid: modified equals created
        valid_campaign2 = Campaign(
            id="campaign--12345678-1234-1234-1234-123456789016",
            created=now,
            modified=now,
            name="Test Campaign 2"
        )
        assert valid_campaign2.created == now
        assert valid_campaign2.modified == now
        
        # Invalid: modified before created
        with pytest.raises(ValueError, match="modified property MUST be later than or equal"):
            Campaign(
                id="campaign--12345678-1234-1234-1234-123456789017",
                created=future,
                modified=past,
                name="Invalid Campaign"
            )


class TestPerformanceOptimizations:
    """Test that optimizations don't break functionality."""
    
    def test_validator_reuse(self):
        """Test that validator reuse across classes works correctly."""
        from stidantic.sdo import Infrastructure, IntrusionSet, Malware, ThreatActor
        
        # Verify all classes have the common validator
        assert hasattr(Campaign, '_validate_last_seen')
        assert hasattr(Infrastructure, '_validate_last_seen')
        assert hasattr(IntrusionSet, '_validate_last_seen')
        assert hasattr(Malware, '_validate_last_seen')
        assert hasattr(ThreatActor, '_validate_last_seen')
        
        # Verify they all work the same way
        now = datetime.now()
        past = now - timedelta(days=1)
        
        # Test Infrastructure
        valid_infra = Infrastructure(
            id="infrastructure--12345678-1234-1234-1234-123456789018",
            created=now,
            modified=now,
            name="Test Infrastructure",
            first_seen=past,
            last_seen=now
        )
        assert valid_infra.first_seen == past
        assert valid_infra.last_seen == now


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
