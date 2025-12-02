#!/usr/bin/env python3
"""
MongoDB Capacity Calculator for BioMuseum
Calculates how many organisms and videos can fit in 512MB
"""

print("="*70)
print("BIOMUSEUM MONGODB CAPACITY ANALYSIS (512 MB LIMIT)")
print("="*70)
print()

# Typical MongoDB document sizes based on schema
TYPICAL_ORGANISM_SIZE = 3.5  # KB - includes taxonomy, descriptions, images
TYPICAL_VIDEO_SIZE = 2.8     # KB - includes metadata, tags, thumbnails

# MongoDB overhead per document (indexes, storage overhead)
MONGODB_OVERHEAD_PERCENT = 1.3  # 30% overhead for indexes and padding

# Space reserved for indexes and system
SYSTEM_RESERVED = 20  # MB

# Total usable space
TOTAL_SPACE_MB = 512
USABLE_SPACE_MB = TOTAL_SPACE_MB - SYSTEM_RESERVED
USABLE_SPACE_KB = USABLE_SPACE_MB * 1024

print(f"Total MongoDB Quota: {TOTAL_SPACE_MB} MB")
print(f"System Reserved: {SYSTEM_RESERVED} MB")
print(f"Usable Space: {USABLE_SPACE_MB} MB ({USABLE_SPACE_KB:.0f} KB)")
print()

# Calculate capacity with overhead
organism_size_with_overhead = TYPICAL_ORGANISM_SIZE * MONGODB_OVERHEAD_PERCENT
video_size_with_overhead = TYPICAL_VIDEO_SIZE * MONGODB_OVERHEAD_PERCENT

max_organisms = int(USABLE_SPACE_KB / organism_size_with_overhead)
max_videos = int(USABLE_SPACE_KB / video_size_with_overhead)

print("INDIVIDUAL CAPACITY:")
print(f"  Avg Organism Size: {TYPICAL_ORGANISM_SIZE} KB (+ {(MONGODB_OVERHEAD_PERCENT-1)*100:.0f}% overhead)")
print(f"  Avg Video Size: {TYPICAL_VIDEO_SIZE} KB (+ {(MONGODB_OVERHEAD_PERCENT-1)*100:.0f}% overhead)")
print()

print("MAXIMUM CAPACITY:")
print(f"  ✓ Maximum Organisms: ~{max_organisms:,}")
print(f"  ✓ Maximum Videos: ~{max_videos:,}")
print()

# Mixed scenario
print("REALISTIC MIXED SCENARIOS:")
print()

scenarios = [
    ("Conservative (1000 organisms + rest videos)", 1000, max_videos - 1000),
    ("Balanced (2000 organisms + rest videos)", 2000, max_videos - 2000),
    ("Video-heavy (500 organisms + rest videos)", 500, max_videos - 500),
]

for scenario_name, orgs, vids in scenarios:
    orgs_space = (orgs * organism_size_with_overhead) / 1024
    vids_space = (vids * video_size_with_overhead) / 1024
    total = orgs_space + vids_space
    print(f"  {scenario_name}")
    print(f"    └─ {orgs:,} organisms ({orgs_space:.1f} MB) + {vids:,} videos ({vids_space:.1f} MB)")
    print(f"       Total: {total:.1f} MB (Used: {(total/USABLE_SPACE_MB)*100:.1f}%)")
    print()

print("GROWTH RECOMMENDATIONS:")
print(f"  • At {TYPICAL_VIDEO_SIZE} KB per video: Can add ~{int(USABLE_SPACE_MB/0.0028):,} videos total")
print(f"  • At {TYPICAL_ORGANISM_SIZE} KB per organism: Can add ~{int(USABLE_SPACE_MB/0.0035):,} organisms total")
print(f"  • Recommended ratio: 10% organisms, 90% videos")
print(f"    └─ ~{int(max_organisms*0.1):,} organisms + ~{int(max_videos*0.9):,} videos")
print()

print("="*70)
print("SUMMARY")
print("="*70)
print(f"With 512 MB MongoDB quota, you can store:")
print(f"  • ~{max_organisms:,} organisms")
print(f"  • ~{max_videos:,} videos")
print(f"  • Or a mix of both within the limit")
print()
print("💡 RECOMMENDATION: Implement data archival or upgrade to larger quota")
print("   if you plan to exceed ~30K videos or ~40K organisms")
print("="*70)
