
import pytest

from bus_transit_fare import (
    process_commute_manifest,
    inspect_smartcard_turnstiles
)


# 1. Test invalid manifest type
def test_invalid_manifest_type():
    with pytest.raises(ValueError):
        process_commute_manifest("invalid", 2.0)


# 2. Test negative booking fee
def test_negative_booking_fee():
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)


# 3. Test inactive route
def test_inactive_route():
    manifests = [
        {
            "route_active": False,
            "route_type": "local"
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 0.0
    assert result["status"] == "ZERO_RIDERSHIP"


# 4. Test express route
def test_express_route():
    manifests = [
        {
            "route_active": True,
            "route_type": "express",
            "commuters": [{"zones": 2, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 8.0
    assert result["status"] == "COMPLETED"


# 5. Test shuttle route
def test_shuttle_route():
    manifests = [
        {
            "route_active": True,
            "route_type": "shuttle",
            "commuters": [{"zones": 2, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 6.0


# 6. Test local route
def test_local_route():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": 2, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 4.5


# 7. Test invalid route
def test_invalid_route():
    manifests = [
        {
            "route_active": True,
            "route_type": "unknown",
            "commuters": []
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 0.0
    assert result["status"] == "ZERO_RIDERSHIP"


# 8. Test student passenger
def test_student_passenger():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": 2, "type": "student"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 1.75


# 9. Test senior passenger
def test_senior_passenger():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": 2, "type": "senior"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 2.45


# 10. Test zero zones
def test_zero_zones():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": 0, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 0.0


# 11. Test negative zones
def test_negative_zones():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": -2, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 0.0


# 12. Test blacklisted local card
def test_blacklisted_local_card():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [
                {"zones": 2, "type": "regular", "blacklisted": True},
                {"zones": 2, "type": "regular", "blacklisted": False}
            ]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 4.5


# 13. Test blacklisted express card
def test_blacklisted_express_card():
    manifests = [
        {
            "route_active": True,
            "route_type": "express",
            "priority_boarding": True,
            "commuters": [
                {"zones": 2, "blacklisted": True},
                {"zones": 3, "type": "regular"}
            ]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 2.0


# 14. Test priority boarding
def test_priority_boarding():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "priority_boarding": True,
            "commuters": [{"zones": 2, "type": "regular"}]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["total_fare"] == 6.5


# 15. Test empty commuters
def test_empty_commuters():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": []
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["status"] == "ZERO_RIDERSHIP"


# 16. Test audit rejected
def test_audit_rejected():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [
                {"zones": 0},
                {"zones": 0},
                {"zones": 0},
                {"zones": 0},
                {"zones": 0}
            ]
        }
    ]

    result = process_commute_manifest(manifests, 2.0)

    assert result["status"] == "AUDIT_REJECTED"


# 17. Test turnstile with no data
def test_turnstile_no_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"
    assert inspect_smartcard_turnstiles(None) == "NO_DATA"


# 18. Test turnstile jam
def test_turnstile_jam():
    matrix = [[4, 5, 1]]

    assert inspect_smartcard_turnstiles(matrix) == "TURNSTILE_JAM"


# 19. Test operational turnstile
def test_turnstile_operational():
    matrix = [
        [1, 2, 4, 1, 5],
        [2, 3, 1]
    ]

    assert inspect_smartcard_turnstiles(matrix) == "OPERATIONAL"


# 20. Test empty device readings
def test_empty_device_readings():
    assert inspect_smartcard_turnstiles([[]]) == "OPERATIONAL"
