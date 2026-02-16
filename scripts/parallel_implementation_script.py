import concurrent.futures
import subprocess
import os
import sys
import time

def run_command(command, description):
    print(f"Starting: {description}...")
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        duration = time.time() - start_time
        print(f"✅ Completed: {description} in {duration:.2f}s")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        print(f"❌ Failed: {description} in {duration:.2f}s")
        print(f"Error output: {e.stderr}")
        return False, e.stderr

def generate_photos():
    prompts = {
        "titan": "Professional headshot of a confident Czech marketing expert named Pavel Kaspar, 40s, business casual attire, clean modern office background, soft studio lighting, high resolution, 4k",
        "nova": "Friendly headshot of a creative marketing strategist named Pavel Kaspar, 40s, smart casual, glass wall office background with sticky notes, warm lighting, approachable smile, high resolution, 4k",
        "lux": "Premium minimal headshot of a senior marketing consultant named Pavel Kaspar, 40s, black turtleneck, clean white background, dramatic lighting, high contrast, monochrome aesthetic, 4k",
        "target": "Focused headshot of a performance marketing expert named Pavel Kaspar, 40s, sharp business suit, abstract data background, cool blue lighting, intense gaze, high resolution, 4k",
        "spark": "Bold headshot of a digital disruptor named Pavel Kaspar, 40s, modern streetwear, neon city background, cyan and magenta rim lighting, confident expression, high resolution, 4k"
    }

    success = True
    generated_count = 0

    # Check what's missing
    required_photos = list(prompts.keys())
    missing = []

    for theme in required_photos:
        path = f"public/images/theme/photo_{theme}.jpg"
        if not os.path.exists(path):
            missing.append(theme)

    if not missing:
        print("ℹ️ All photos exist. Skipping generation.")
        return True, "All photos present"

    print(f"Generate Photos: Generating {len(missing)} missing photos: {', '.join(missing)}")

    for theme in missing:
        cmd = f'python scripts/generate_images.py --provider nvidia --output public/images/theme/photo_{theme}.jpg --prompt "{prompts[theme]}"'
        result, output = run_command(cmd, f"Generating photo for {theme}")
        if result:
            generated_count += 1
        else:
            print(f"❌ Failed to generate {theme}")
            success = False

    return success, f"Photo generation completed ({generated_count}/{len(missing)})"

def run_checks():
    return run_command("npm run lint && npm run format:check", "Code Quality Checks (Lint/Format)")

def run_unit_tests():
    return run_command("npm run test:unit", "Unit Tests (Vitest)") # Assuming test:unit exists or just test

def build_site():
    return run_command("npm run build", "Astro Build")

def run_visual_tests():
    return run_command("npx playwright test tests/e2e/visual/debug.spec.ts --project=chromium", "Visual Verification (Playwright)")

def main():
    print("🚀 Starting Parallel Implementation & Verification Sequence")
    print("=======================================================")

    start_all = time.time()

    # Phase 1: Parallel Execution (Safe independent tasks)
    print("\n[Phase 1] Parallel Execution: Photos, Linting, Unit Tests")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_photos = executor.submit(generate_photos)
        future_checks = executor.submit(run_checks)
        # Using 'npm run test' which runs all tests, including unit.
        # If there's a specific unit test script, change here.
        future_tests = executor.submit(run_command, "npm run test", "All Tests (Vitest)")

        # Wait for all
        photo_success, photo_msg = future_photos.result()
        check_success, check_msg = future_checks.result()
        test_success, test_msg = future_tests.result()

    # Checks (Lint) are non-blocking for now as we fix ESLint config
    if not (photo_success and test_success):
        print("\n❌ Phase 1 Failed (Photos or Tests). Stopping sequence.")
        print(f"Photos: {photo_success}, Checks: {check_success} (Warning), Tests: {test_success}")
        sys.exit(1)

    if not check_success:
        print(f"\n⚠️ Warning: Code Quality Checks failed with message: {check_msg}. Proceeding anyway.")

    print("\n✅ Phase 1 Complete. Proceeding to Build & Verify.")

    # Phase 2: Build (Depends on assets & code quality)
    print("\n[Phase 2] Building Site")
    build_success, _ = build_site()
    if not build_success:
        print("\n❌ Build Failed. Stopping.")
        sys.exit(1)

    # Phase 3: Visual Verification (Depends on build)
    print("\n[Phase 3] Visual Verification")
    visual_success, _ = run_visual_tests()
    if not visual_success:
        print("\n❌ Visual Verification Failed.")
        sys.exit(1)

    total_duration = time.time() - start_all
    print(f"\n🎉 All Systems Go! Site is ready for deployment. (Total time: {total_duration:.2f}s)")

if __name__ == "__main__":
    main()
