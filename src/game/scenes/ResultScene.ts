import Phaser from 'phaser';
import type { RunSnapshot } from '../../state/RunState';

export class ResultScene extends Phaser.Scene {
  constructor() {
    super('ResultScene');
  }

  create(data: RunSnapshot): void {
    const { width, height } = this.scale;
    this.cameras.main.setBackgroundColor('#050705');
    this.add.text(width / 2, 118, 'RUN AUTOPSY', {
      fontFamily: 'monospace', fontSize: '18px', color: '#ff2b91', letterSpacing: 4,
    }).setOrigin(0.5);

    this.add.text(width / 2, 210, data.kills > 0 ? 'RUGGED.' : 'LIQUIDATED.', {
      fontFamily: 'Impact, sans-serif', fontSize: '88px', color: '#f4f7ef',
    }).setOrigin(0.5);

    this.add.text(width / 2, 320, `${data.score.toLocaleString()} SCORE   //   ${data.kills} KILLS`, {
      fontFamily: 'monospace', fontSize: '24px', color: '#c8ff28',
    }).setOrigin(0.5);

    const retry = this.add.rectangle(width / 2, 420, 300, 64, 0xc8ff28).setInteractive({ useHandCursor: true });
    this.add.text(width / 2, 420, 'RUN IT BACK →', {
      fontFamily: 'Impact, sans-serif', fontSize: '24px', color: '#050705',
    }).setOrigin(0.5);
    retry.on('pointerdown', () => this.scene.start('GameScene'));

    const menu = this.add.text(width / 2, 492, 'BACK TO MENU', {
      fontFamily: 'monospace', fontSize: '15px', color: '#25d5ff',
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });
    menu.on('pointerdown', () => this.scene.start('MenuScene'));

    this.add.text(width / 2, height - 42, 'BUILD 1.0-alpha.1 // COMBAT LOOP FIRST // ART LATER', {
      fontFamily: 'monospace', fontSize: '13px', color: '#596359',
    }).setOrigin(0.5);
  }
}
