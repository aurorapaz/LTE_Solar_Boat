import { Component } from '@angular/core';
import { Toast, ToastrService, ToastPackage } from 'ngx-toastr';

@Component({
    selector: '[pink-toast-component]',
    template: `
    <button *ngIf="options.closeButton" (click)="remove()" class="toast-close-button" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    <div *ngIf="title" [class]="options.titleClass" [attr.aria-label]="title">
      {{ title }} <ng-container *ngIf="duplicatesCount">[{{ duplicatesCount + 1 }}]</ng-container>
    </div>
    <div *ngIf="message && options.enableHtml" role="alertdialog" aria-live="polite"
      [class]="options.messageClass" [innerHTML]="message">
    </div>
    <div *ngIf="message && !options.enableHtml" role="alertdialog" aria-live="polite"
      [class]="options.messageClass" [attr.aria-label]="message">
      {{ message }}
    </div>
    <div>
      <br/><a id="send" (click)="action($event)" class='btn btn-danger'>Send Alarm</a>
      <a type="button" (click)="action($event)" class='btn btn-warning'>Ignore Alarm</a>
    </div>
    <div *ngIf="options.progressBar">
      <div class="toast-progress" [style.width]="width + '%'"></div>
    </div>
    `,
    preserveWhitespaces: true,
})
export class CustomToast extends Toast {
    // used for demo purposes
    undoString = 'undo';
    // constructor is only necessary when not using AoT
    constructor(
        protected toastrService: ToastrService,
        public toastPackage: ToastPackage,
    ) {
        super(toastrService, toastPackage);
    }

    action(event) {
      event.stopPropagation();
      this.toastPackage.triggerAction(event.target.id);
      this.remove();
      //this.toastrService.clear();
      return false;
    }
}