from dataclasses import dataclass


@dataclass
class SceneConfig:
    sanctum_size: float = 60.0
    step_count: int = 3
    step_width: float = 12.0
    step_depth: float = 3.0
    step_height: float = 0.45
    platform_width: float = 14.0
    platform_depth: float = 8.0
    platform_height: float = 0.7
    wall_width: float = 23.0
    wall_height: float = 16.0
    wall_depth: float = 1.2
    pillar_radius: float = 0.55
    pillar_height: float = 8.0
    pillar_segments: int = 24
    camera_lens_mm: float = 50.0
    camera_location: tuple = (0.0, -28.0, 3.2)
    camera_rotation_deg: tuple = (82.0, 0.0, 0.0)
    sun_energy: float = 1.2
    sun_angle_deg: float = 5.0
    area_energy: float = 250.0
    area_size: float = 6.0


DEFAULT_CONFIG = SceneConfig()
