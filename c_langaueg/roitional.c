#include <stdio.h>

int main()
{
    int a[] = {0, 3, 6, 9, 12, 14, 18, 20, 22, 25, 27};
    int l = sizeof(a) / sizeof(a[0]);
    int t, r;

    printf("Enter the rotation number: ");
    scanf("%d", &r);

    for (int i = 0; i < r; i++)
    {
        t = a[0];
        for (int j = 0; j < l - 1; j++)
        {
            a[j] = a[j + 1];
        }
        a[l - 1] = t;
    }

    // طباعة المصفوفة بعد التدوير
    for (int i = 0; i < l; i++) {
        printf("%d ", a[i]);
    }

    return 0;
}