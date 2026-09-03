import Phaser from 'phaser';

export class MenuScene extends Phaser.Scene {
  constructor() {
    super('MenuScene');
  }

  create(): void {
    const { width, height } = this.scale;
    this.cameras.main.setBackgroundColor('#050705');

    this.add.text(width / 2, 112, 'GRAMLEEK // BUILD 1.0', {
      fontFamily: 'monospace', fontSize: '18px', color: '#25d5ff', letterSpacing: 3,
    }).setOrigin(0.5);

    this.add.text(width / 2, 212, 'LEEKed IN', {
      fontFamily: 'Impact, sans-serif', fontSize: '94px', color: '#c8ff28', stroke: '#050705', strokeThickness: 8,
    }).setOrigin(0.5);

    this.add.text(width / 2, 295, 'PHASER 4 VERTICAL SLICE // NO TOKEN BURN', {
      fontFamily: 'monospace', fontSize: '16px', color: '#aab5aa',
    }).setOrigin(0.5);

    const button = this.add.rectangle(width / 2, 390, 320, 68, 0xffe600)
      .setInteractive({ useHandCursor: true });
    const label = this.add.text(width / 2, 390, 'ENTER LIQUIDITY ALLEY →', {
      fontFamily: 'Impact, sans-serif', fontSize: '24px', color: '#050705',
    }).setOrigin(0.5);

    button.on('pointerover', () => button.setFillStyle(0xc8ff28));
    button.on('pointerout', () => button.setFillStyle(0xffe600));
    button.on('pointerdown', () => this.scene.start('GameScene'));
    label.setDepth(2);

    this.add.text(width / 2, height - 58, 'WASD / ARROWS TO MOVE · POINTER TO AIM · AUTO-FIRE', {
      fontFamily: 'monospace', fontSize: '14px', color: '#667066',
    }).setOrigin(0.5);
  }
}
