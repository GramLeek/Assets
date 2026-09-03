type TelegramWebApp = {
  ready?: () => void;
  expand?: () => void;
  HapticFeedback?: {
    impactOccurred?: (style: 'light' | 'medium' | 'heavy') => void;
    notificationOccurred?: (type: 'success' | 'error' | 'warning') => void;
  };
  initDataUnsafe?: {
    start_param?: string;
    user?: { id?: number; username?: string; first_name?: string };
  };
};

declare global {
  interface Window {
    Telegram?: { WebApp?: TelegramWebApp };
  }
}

export const TelegramBridge = {
  get app(): TelegramWebApp | undefined {
    return window.Telegram?.WebApp;
  },

  init(): void {
    this.app?.ready?.();
    this.app?.expand?.();
  },

  startParam(): string | undefined {
    return this.app?.initDataUnsafe?.start_param;
  },

  hit(): void {
    this.app?.HapticFeedback?.impactOccurred?.('light');
  },

  kill(): void {
    this.app?.HapticFeedback?.notificationOccurred?.('success');
  },
};
