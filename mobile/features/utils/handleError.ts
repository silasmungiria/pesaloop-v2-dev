import { useNotificationToast } from "@/features/providers";

export function handleError(
  error: unknown,
  fallbackMessage = "Something went wrong. Please try again later."
) {
  const { showNotification } = useNotificationToast();

  // Default error message
  let errorMessage = fallbackMessage;

  if (typeof error === "string") {
    errorMessage = error;
  } else if (error instanceof Error) {
    errorMessage = error.message;
  } else if (error && typeof error === "object" && "message" in error) {
    errorMessage = String((error as any).message);
  }

  showNotification(errorMessage, "error", 6000);
}
