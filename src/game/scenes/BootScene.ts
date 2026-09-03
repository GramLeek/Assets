import Phaser from 'phaser';
import { TelegramBridge } from '../../telegram/TelegramBridge';

export class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  create(): void {
    TelegramBridge.init();
    this.createPlaceholderTextures();
    this.scene.start('MenuScene');
  }

  private createPlaceholderTextures(): void {
    const g = this.add.graphics();

    g.fillStyle(0xc8ff28, 1);
    g.fillCircle(24, 24, 18);
    g.fillStyle(0x050705, 1);
    g.fillRect(18, 8, 12, 31);
    g.generateTexture('player', 48, 48);
    g.clear();

    g.fillStyle(0xff2b91, 1);
    g.fillRoundedRect(4, 4, 40, 40, 9);
    g.fillStyle(0x050705, 1);
    g.fillRect(13, 16, 22, 5);
    g.fillRect(13, 27, 22, 5);
    g.generateTexture('bot', 48, 48);
    g.clear();

    g.fillStyle(0xffe600, 1);
    g.fillCircle(6, 6, 6);
    g.generateTexture('bullet', 12, 12);
    g.clear();

    g.fillStyle(0x1a231a, 1);
    g.fillRect(0, 0, 32, 32);
    g.lineStyle(1, 0x344234, 1);
    g.strokeRect(0, 0, 32, 32);
    g.generateTexture('floor', 32, 32);
    g.clear();

    g.fillStyle(0x384438, 1);
    g.fillRect(0, 0, 32, 32);
    g.generateTexture('wall', 32, 32);
    g.destroy();
  }
}
