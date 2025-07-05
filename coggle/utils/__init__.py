from kaggle import api
from time import sleep
from kagglesdk.kernels.types.kernels_enums import KernelWorkerStatus

def wait_for_kernel_to_finish(kernel_id: str, max_tries=50, wait_sec=10):
    print("[Info] Waiting for kernel to finish...", end='')

    for _ in range(max_tries):
        try:
            status_obj = api.kernels_status(kernel_id)
            current_status = getattr(status_obj, "status", "")
            failure_msg = getattr(status_obj, "failureMessage", "")
            if current_status == KernelWorkerStatus.COMPLETE:
                print("\n[Info] Kernel execution complete.")
                return True
            elif current_status == KernelWorkerStatus.ERROR:
                print(f"\n[Error] Kernel failed: {failure_msg}")
                return False
            else:
                print(".", end='')

        except Exception as e:
            print(f"[Warning] Could not fetch kernel status: {e}")

        try:
            sleep(wait_sec)
        except KeyboardInterrupt:
            print("[Warning] Interrupted by user.")
            return False

    print("[Warning] Timeout: Kernel is still running.")
    return False